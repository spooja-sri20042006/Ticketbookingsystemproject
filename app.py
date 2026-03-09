from flask import Flask, render_template, request, redirect, session, jsonify
from config import users_table, bookings_table, reviews_table, create_tables
from datetime import datetime
from decimal import Decimal
import uuid

app = Flask(__name__)
app.secret_key = 'travelgo_secret_key_2026'

# Create tables on startup
with app.app_context():
    try:
        create_tables()
    except Exception as e:
        print(f"Table creation: {e}")

# ── Home ──
@app.route('/')
def index():
    return render_template('index.html')

# ── Register ──
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form.get('name')
        email    = request.form.get('email')
        password = request.form.get('password')

        # Check existing user
        response = users_table.get_item(Key={'email': email})
        if 'Item' in response:
            return render_template('register.html', error='Email already registered!')

        users_table.put_item(Item={
            'email':      email,
            'name':       name,
            'password':   password,
            'created_at': str(datetime.now())
        })
        return redirect('/login')
    return render_template('register.html')

# ── Login ──
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')

        response = users_table.get_item(Key={'email': email})
        user = response.get('Item')

        if user and user['password'] == password:
            session['user']  = email
            session['name']  = user['name']
            session['email'] = email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid email or password!')
    return render_template('login.html')

# ── Logout ──
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ── Dashboard ──
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', name=session.get('name'))

# ── Profile ──
@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')
    response = users_table.get_item(Key={'email': session.get('email')})
    user = response.get('Item', {})
    return render_template('profile.html', user=user)

# ── Notifications ──
@app.route('/notifications')
def notifications():
    if 'user' not in session:
        return redirect('/login')
    return render_template('notifications.html')

# ── Offers ──
@app.route('/offers')
def offers():
    if 'user' not in session:
        return redirect('/login')
    offers_list = [
        {'destination': 'Dubai',     'discount': '30%', 'price': '$599'},
        {'destination': 'Bali',      'discount': '25%', 'price': '$499'},
        {'destination': 'Paris',     'discount': '20%', 'price': '$799'},
        {'destination': 'Singapore', 'discount': '15%', 'price': '$649'},
        {'destination': 'Tokyo',     'discount': '18%', 'price': '$899'},
        {'destination': 'Bangkok',   'discount': '35%', 'price': '$349'},
    ]
    return render_template('offers.html', offers=offers_list)

# ── Tips ──
@app.route('/tips')
def tips():
    if 'user' not in session:
        return redirect('/login')
    tips_list = [
        {'icon': '🎒', 'title': 'Pack Light',          'description': 'Travel with only a carry-on to save time and money on baggage fees.'},
        {'icon': '💳', 'title': 'Use Travel Cards',    'description': 'Get a no-foreign-transaction-fee card to save money abroad.'},
        {'icon': '🌍', 'title': 'Learn Local Phrases', 'description': 'Even a few words in the local language opens doors and hearts.'},
        {'icon': '📱', 'title': 'Offline Maps',        'description': 'Download Google Maps offline before you arrive.'},
        {'icon': '🏨', 'title': 'Book in Advance',     'description': 'Save up to 40% by booking hotels at least 3 weeks early.'},
        {'icon': '✈️', 'title': 'Flexible Dates',      'description': 'Flying mid-week is usually 20-30% cheaper than weekends.'},
    ]
    return render_template('tips.html', tips=tips_list)

# ── Search & Book ──
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        source      = request.form.get('source')
        destination = request.form.get('destination')
        date        = request.form.get('date')
        travelers   = request.form.get('travelers')
        transport   = request.form.get('transport')
        budget      = request.form.get('budget')

        try:
            travel_date = datetime.strptime(date, '%Y-%m-%d')
            if travel_date < datetime.now():
                return render_template('search.html', error='Please select a future date!')
        except:
            return render_template('search.html', error='Invalid date format!')

        booking_id = str(uuid.uuid4())[:8].upper()
        bookings_table.put_item(Item={
            'user_id':     session['user'],
            'booking_id':  booking_id,
            'source':      source,
            'destination': destination,
            'date':        date,
            'travelers':   travelers,
            'transport':   transport,
            'budget':      budget,
            'status':      'confirmed',
            'created_at':  str(datetime.now())
        })
        return redirect('/bookings')
    return render_template('search.html')

# ── Bookings ──
@app.route('/bookings')
def my_bookings():
    if 'user' not in session:
        return redirect('/login')
    from boto3.dynamodb.conditions import Key
    response = bookings_table.query(
        KeyConditionExpression=Key('user_id').eq(session['user'])
    )
    user_bookings = response.get('Items', [])
    return render_template('bookings.html', bookings=user_bookings)

# ── AI Chatbot ──
@app.route('/chatbot')
def chatbot():
    if 'user' not in session:
        return redirect('/login')
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data    = request.get_json()
    message = data.get('message', '').lower()
    responses = {
        'japan':     '🇯🇵 Japan is amazing! Best time: March-May. Must visit: Tokyo, Kyoto, Osaka. Budget: ~$100/day.',
        'paris':     '🇫🇷 Paris — city of love! Eiffel Tower, Louvre. Best time: April-June. Budget: ~$150/day.',
        'dubai':     '🇦🇪 Dubai — luxury at its best! Burj Khalifa, desert safari. Best time: Nov-Mar.',
        'bali':      '🇮🇩 Bali is paradise! Ubud, Seminyak, temples. Best time: April-October.',
        'budget':    '💰 Budget tips: Book 3+ weeks early, fly mid-week, eat local food!',
        'pack':      '🎒 Pack: universal adapter, travel pillow, portable charger, travel insurance!',
        'flight':    '✈️ Best deals: Google Flights, fly Tuesdays/Wednesdays, book 6-8 weeks early!',
        'visa':      '🛂 Visa tip: Apply 4-6 weeks early, keep bank statements ready!',
        'thailand':  '🇹🇭 Thailand — visa free for Indians! Bangkok, Phuket. Budget: ~$50/day.',
        'singapore': '🇸🇬 Singapore — clean, safe, amazing food! Budget: ~$100/day.',
    }
    reply = '🤖 Ask me about Japan, Paris, Dubai, Bali, Thailand or budget tips, packing, flights, visas!'
    for keyword, response in responses.items():
        if keyword in message:
            reply = response
            break
    return jsonify({'reply': reply})

# ── Interactive Map ──
@app.route('/map')
def map_view():
    if 'user' not in session:
        return redirect('/login')
    return render_template('map.html')

# ── Reviews ──
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        destination = request.form.get('destination')
        rating      = request.form.get('rating', '5')
        review_text = request.form.get('review')
        review_id   = str(uuid.uuid4())

        reviews_table.put_item(Item={
            'review_id':   review_id,
            'user_name':   session.get('name'),
            'destination': destination,
            'rating':      int(rating),
            'review':      review_text,
            'created_at':  str(datetime.now())
        })
        return redirect('/reviews')

    response    = reviews_table.scan()
    all_reviews = response.get('Items', [])
    sample_reviews = [
        {'user_name': 'Raj M.',   'destination': 'Tokyo',     'rating': 5, 'review': 'Tokyo exceeded all expectations!'},
        {'user_name': 'Sara K.',  'destination': 'Bali',      'rating': 4, 'review': 'Bali is paradise on earth!'},
        {'user_name': 'Ahmed R.', 'destination': 'Dubai',     'rating': 5, 'review': 'Dubai desert safari was the highlight!'},
        {'user_name': 'Meera T.', 'destination': 'Paris',     'rating': 4, 'review': 'Paris was magical!'},
        {'user_name': 'Kiran P.', 'destination': 'Singapore', 'rating': 5, 'review': 'Singapore blew my mind!'},
    ]
    combined = all_reviews + sample_reviews
    return render_template('reviews.html', reviews=combined)

# ── Analytics ──
@app.route('/analytics')
def analytics():
    if 'user' not in session:
        return redirect('/login')
    return render_template('analytics.html')

@app.route('/api/booking-stats')
def booking_stats():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    from boto3.dynamodb.conditions import Key
    response = bookings_table.query(
        KeyConditionExpression=Key('user_id').eq(session['user'])
    )
    total = len(response.get('Items', []))
    return jsonify({'total_bookings': total})

# ── Weather ──
@app.route('/weather')
def weather():
    if 'user' not in session:
        return redirect('/login')
    return render_template('weather.html')

# ── Currency ──
@app.route('/currency')
def currency():
    if 'user' not in session:
        return redirect('/login')
    return render_template('currency.html')

# ── Trip Planner ──
@app.route('/planner')
def planner():
    if 'user' not in session:
        return redirect('/login')
    return render_template('planner.html')

# ── Travel Quiz ──
@app.route('/quiz')
def quiz():
    if 'user' not in session:
        return redirect('/login')
    return render_template('quiz.html')

# ── Photo Gallery ──
@app.route('/gallery')
def gallery():
    if 'user' not in session:
        return redirect('/login')
    return render_template('gallery.html')

# ── Visa Checker ──
@app.route('/visa')
def visa():
    if 'user' not in session:
        return redirect('/login')
    return render_template('visa.html')

# ── Price Tracker ──
@app.route('/pricetracker')
def pricetracker():
    if 'user' not in session:
        return redirect('/login')
    return render_template('pricetracker.html')

# ── Loyalty & Referrals ──
@app.route('/loyalty')
def loyalty():
    if 'user' not in session:
        return redirect('/login')
    return render_template('loyalty.html')

if __name__ == '__main__':

    


app.run(host="0.0.0.0", port=5000, debug=True)

