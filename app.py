from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลทริป 1 วันในเชียงใหม่ (พิกัด, รูปภาพ, คำบรรยาย)
LOCATIONS = [
    {
        "id": "maya",
        "name": "เมญ่า ไลฟ์สไตล์ ชอปปิง เซ็นเตอร์",
        "english_name": "MAYA Lifestyle Shopping Center",
        "category": "Shopping & Lifestyle",
        "lat": 18.801747307507746,
        "lng": 98.96801603211877,
        "image": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?q=80&w=1000&auto=format&fit=crop",
        "description": "https://storage.googleapis.com/tatstar-org-prod-assets-public/users/1221/company/cover/1724913627792.jpg",
        "time": "09:30 AM"
    },
    {
        "id": "wat-chiang-man",
        "name": "วัดเชียงมั่น",
        "english_name": "Wat Chiang Man",
        "category": "Historical & Temple",
        "lat": 18.793811972947193,
        "lng": 98.98942993880435,
        "image": "https://images.unsplash.com/photo-1609949279531-cf48d64bed89?q=80&w=1000&auto=format&fit=crop",
        "description": "สัมผัสประวัติศาสตร์อันเก่าแก่ที่สุดในเมืองเชียงใหม่ วัดแรกที่สร้างขึ้นพร้อมกับการสถาปนาเวียงเชียงใหม่ ชมเจดีย์เหลี่ยมช้างล้อมอันรงคุณค่าและสงบเงียบ",
        "time": "11:30 AM"
    },
    {
        "id": "wat-phra-singh",
        "name": "วัดพระสิงห์วรมหาวิหาร",
        "english_name": "Wat Phra Singh",
        "category": "Culture & Heritage",
        "lat": 18.788469902639783,
        "lng": 98.98219254530527,
        "image": "https://images.unsplash.com/photo-1528181304800-259b08848526?q=80&w=1000&auto=format&fit=crop",
        "description": "กราบพระพุทธสิหิงค์ พระพุทธรูปคู่บ้านคู่เมืองเชียงใหม่ ชมจิตรกรรมฝาผนังลายคำล้านนาโบราณในวิหารลายคำ สะท้อนความงดงามทางศิลปวัฒนธรรมอันประณีต",
        "time": "02:00 PM"
    },
    {
        "id": "transport-office",
        "name": "สำนักงานขนส่งจังหวัดเชียงใหม่แห่งที่ 1",
        "english_name": "Chiang Mai Transport Office (Station 1)",
        "category": "Transit & Landmark",
        "lat": 18.766837248800318,
        "lng": 99.00561186540699,
        "image": "https://images.unsplash.com/photo-1508873696983-2df515122519?q=80&w=1000&auto=format&fit=crop",
        "description": "จุดเชื่อมต่อการเดินทางสำคัญของเมืองเชียงใหม่ สัมผัสวิถีชีวิตผู้คนและการสัญจรแบบท้องถิ่น ย้อนรอยเส้นทางคมนาคมเดิมของเมือง",
        "time": "04:30 PM"
    },
    {
        "id": "airport",
        "name": "ท่าอากาศยานนานาชาติเชียงใหม่",
        "english_name": "Chiang Mai International Airport",
        "category": "Departure & Sunset",
        "lat": 18.772023143524223,
        "lng": 98.96903065610294,
        "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=1000&auto=format&fit=crop",
        "description": "ส่งท้ายทริปวันเดียวด้วยภาพความประทับใจ ณ ประตูสู่ภาคเหนือของไทย เตรียมพร้อมสำหรับการเดินทางกลับพร้อมความทรงจำอันมีค่า",
        "time": "06:30 PM"
    }
]

@app.route('/')
def index():
    # ค่ากลางของพิกัดเชียงใหม่เพื่อโฟกัสแผนที่
    center_lat = 18.7845
    center_lng = 98.9815

    # สร้างแผนที่ Folium พร้อมเลือกไทล์สไตล์โทนอุ่นและวินเทจ (CartoDB Positron)
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=13,
        tiles='CartoDB positron'
    )

    route_points = []
    
    # เพิ่ม Marker สำหรับแต่ละสถานที่
    for idx, loc in enumerate(LOCATIONS, 1):
        coord = [loc["lat"], loc["lng"]]
        route_points.append(coord)
        
        # ป๊อบอัพในแผนที่
        popup_html = f"""
        <div style="font-family: 'Playfair Display', serif; text-align: center; width: 180px;">
            <b style="font-size: 14px; color: #2c2a29;">{idx}. {loc['name']}</b><br>
            <span style="font-size: 11px; color: #8c8275;">{loc['time']}</span>
        </div>
        """
        
        folium.Marker(
            location=coord,
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"{idx}. {loc['name']}",
            icon=folium.Icon(color='darkred' if idx==1 else ('cadetblue' if idx==len(LOCATIONS) else 'black'), icon='info-sign')
        ).add_to(m)

    # วาดเส้นทางการเดินทาง (Polyline) เชื่อมต่อจุดต่างๆ
    folium.PolyLine(
        route_points,
        color="#8B5A2B",
        weight=3,
        opacity=0.7,
        dash_array='5, 10'
    ).add_to(m)

    # แปลงแผนที่ Folium เป็น HTML String
    map_html = m._repr_html_()

    return render_template('index.html', locations=LOCATIONS, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)