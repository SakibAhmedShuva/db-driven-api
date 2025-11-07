from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Configuration from environment
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
API_TOKEN = os.getenv('API_TOKEN')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Authentication Decorator
def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid authorization header"}), 401
        
        token = auth_header.split(' ')[1]
        if token != API_TOKEN:
            return jsonify({"error": "Invalid API token"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        supabase.table('users').select('id').limit(1).execute()
        return jsonify({
            "status": "healthy",
            "version": "1.0.0",
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "version": "1.0.0",
            "database": "disconnected",
            "error": str(e)
        }), 503

@app.route('/api/categories', methods=['GET'])
@require_token
def get_categories():
    """Get all categories as ID: Name mapping"""
    try:
        response = supabase.table('categories').select('*').execute()
        
        # Convert to ID: Name mapping
        categories = {str(cat['id']): cat['name'] for cat in response.data}
        
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch categories: {str(e)}"}), 500

@app.route('/api/locations', methods=['GET'])
@require_token
def get_locations():
    """Get all locations as ID: Name mapping"""
    try:
        response = supabase.table('locations').select('*').execute()
        
        # Convert to ID: Name mapping
        locations = {str(loc['id']): loc['name'] for loc in response.data}
        
        return jsonify(locations), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch locations: {str(e)}"}), 500

@app.route('/api/search', methods=['GET'])
@require_token
def search_companies():
    """
    Search for companies by category, location, and optional search term
    Query Parameters:
    - category_id: Category ID (required)
    - location_id: Location ID (required)
    - search_term: Optional search term
    """
    try:
        category_id = request.args.get('category_id')
        location_id = request.args.get('location_id')
        search_term = request.args.get('search_term', '').lower().strip()
        
        if not category_id or not location_id:
            return jsonify({"error": "category_id and location_id are required"}), 400
        
        # Build query
        query = supabase.table('companies').select('*')
        
        # Filter by category and location
        query = query.eq('category_id', int(category_id))
        query = query.eq('location_id', int(location_id))
        
        # Execute query
        response = query.execute()
        results = response.data
        
        # If search term provided, filter by keywords or name/description
        if search_term and results:
            filtered_results = []
            for company in results:
                # Check in company name
                if search_term in company.get('company_name', '').lower():
                    filtered_results.append(company)
                    continue
                
                # Check in description
                if search_term in company.get('description', '').lower():
                    filtered_results.append(company)
                    continue
                
                # Check in keywords (if it's a JSON array)
                keywords = company.get('keywords', [])
                if isinstance(keywords, list):
                    if any(search_term in kw.lower() for kw in keywords):
                        filtered_results.append(company)
            
            results = filtered_results
        
        # Sort by advertising tier
        tier_order = {"Premium": 1, "Enhanced": 2, "Logo": 3, "Free": 4}
        results.sort(key=lambda x: tier_order.get(x.get('advertising_tier', 'Free'), 5))
        
        # Format response
        clean_results = [
            {
                "CompanyName": company.get('company_name'),
                "Description": company.get('description'),
                "WebsiteLink": company.get('website_link'),
                "AdvertisingTier": company.get('advertising_tier')
            }
            for company in results
        ]
        
        return jsonify(clean_results), 200
        
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route('/api/user/status', methods=['GET'])
@require_token
def get_user_status():
    """
    Get user subscription status
    Query Parameters:
    - phone_number: User's phone number
    """
    try:
        phone_number = request.args.get('phone_number')
        
        if not phone_number:
            return jsonify({"error": "phone_number is required"}), 400
        
        # Fetch user from database
        response = supabase.table('users').select('*').eq('phone_number', phone_number).execute()
        
        if not response.data:
            # Return default free tier for unknown users
            return jsonify({
                "phone_number": phone_number,
                "status": "free",
                "queries_today": 0,
                "max_queries": 10,
                "queries_remaining": 10
            }), 200
        
        user = response.data[0]
        
        return jsonify({
            "phone_number": phone_number,
            "status": user.get('subscription_tier', 'free'),
            "queries_today": user.get('queries_today', 0),
            "max_queries": user.get('max_daily_queries', 10),
            "queries_remaining": user.get('max_daily_queries', 10) - user.get('queries_today', 0)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to fetch user status: {str(e)}"}), 500

@app.route('/api/stats', methods=['GET'])
@require_token
def get_stats():
    """Get system statistics (for internal use)"""
    try:
        # Count records from each table
        categories_count = supabase.table('categories').select('id', count='exact').execute()
        locations_count = supabase.table('locations').select('id', count='exact').execute()
        companies_count = supabase.table('companies').select('id', count='exact').execute()
        users_count = supabase.table('users').select('id', count='exact').execute()
        
        return jsonify({
            "total_categories": categories_count.count,
            "total_locations": locations_count.count,
            "total_companies": companies_count.count,
            "total_users": users_count.count
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to fetch stats: {str(e)}"}), 500

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Validate environment variables
    if not all([SUPABASE_URL, SUPABASE_KEY, API_TOKEN]):
        print("ERROR: Missing required environment variables!")
        print("Please ensure SUPABASE_URL, SUPABASE_SERVICE_KEY, and API_TOKEN are set in .env")
        exit(1)
    
    app.run(debug=True, host='0.0.0.0', port=5000)