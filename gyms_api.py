import os
import psycopg2
from flask import Blueprint, jsonify, request
from datetime import datetime

gyms_api_app = Blueprint('gyms_api_app', __name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@gyms_api_app.route('/gyms', methods=['GET'])
def get_gyms():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        city = request.args.get('city')
        state = request.args.get('state')
        country = request.args.get('country')
        name = request.args.get('name')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)

        offset = (page - 1) * page_size

        query = "SELECT * FROM gyms WHERE TRUE"
        params = []

        if city:
            query += " AND city = %s"
            params.append(city)
        if state:
            query += " AND state = %s"
            params.append(state)
        if country:
            query += " AND country = %s"
            params.append(country)
        if name:
            query += " AND name ILIKE %s"
            params.append(f"%{name}%")

        query += " LIMIT %s OFFSET %s"
        params.extend([page_size, offset])

        cur.execute(query, params)
        gyms = cur.fetchall()

        gym_list = []
        for gym in gyms:
            gym_data = {
                'gym_id': gym[0],
                'name': gym[1],
                'description': gym[2],
                'address': gym[3],
                'city': gym[4],
                'state': gym[5],
                'country': gym[6],
                'zip_code': gym[7],
                'contact_email': gym[8],
                'contact_phone': gym[9],
                'website_url': gym[10],
                'logo_url': gym[11],
                'created_at': gym[12].isoformat() if gym[12] else None,
                'updated_at': gym[13].isoformat() if gym[13] else None,
            }
            gym_list.append(gym_data)

        return jsonify(gym_list), 200

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if conn:
            cur.close()
            conn.close()