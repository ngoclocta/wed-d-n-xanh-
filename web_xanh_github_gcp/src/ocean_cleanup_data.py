# Dữ liệu cho trò chơi "Nhặt rác thải dưới đại dương"

# Các loại rác thải trong đại dương
OCEAN_WASTE_TYPES = {
    'plastic_bottle': {
        'name': 'Chai nhựa',
        'points': 10,
        'icon': '🍼',
        'color': '#3498db',
        'description': 'Chai nhựa có thể tồn tại 450 năm trong đại dương'
    },
    'plastic_bag': {
        'name': 'Túi nilon',
        'points': 8,
        'icon': '🛍️',
        'color': '#e74c3c',
        'description': 'Túi nilon thường bị nhầm lẫn với thức ăn của rùa biển'
    },
    'food_waste': {
        'name': 'Rác thải sinh hoạt',
        'points': 5,
        'icon': '🗑️',
        'color': '#f39c12',
        'description': 'Rác thải sinh hoạt gây ô nhiễm và thu hút vi khuẩn có hại'
    },
    'fishing_net': {
        'name': 'Lưới đánh cá',
        'points': 15,
        'icon': '🕸️',
        'color': '#9b59b6',
        'description': 'Lưới đánh cá bỏ hoang có thể bẫy và giết chết động vật biển'
    },
    'cigarette_butt': {
        'name': 'Đầu lọc thuốc lá',
        'points': 3,
        'icon': '🚬',
        'color': '#95a5a6',
        'description': 'Đầu lọc thuốc lá chứa hóa chất độc hại và không phân hủy'
    },
    'metal_can': {
        'name': 'Lon kim loại',
        'points': 12,
        'icon': '🥫',
        'color': '#34495e',
        'description': 'Lon kim loại có thể tái chế 100% và tiết kiệm năng lượng'
    }
}

# Câu hỏi môi trường cho trò chơi
ENVIRONMENTAL_QUESTIONS = [
    {
        'id': 1,
        'question': 'Chai nhựa cần bao nhiêu năm để phân hủy hoàn toàn trong đại dương?',
        'options': ['50 năm', '150 năm', '450 năm', '1000 năm'],
        'correct': 2,
        'explanation': 'Chai nhựa cần khoảng 450 năm để phân hủy hoàn toàn, gây ô nhiễm nghiêm trọng cho đại dương.'
    },
    {
        'id': 2,
        'question': 'Loại rác thải nào chiếm tỷ lệ cao nhất trong đại dương?',
        'options': ['Chai nhựa', 'Túi nilon', 'Lưới đánh cá', 'Vi nhựa'],
        'correct': 3,
        'explanation': 'Vi nhựa (microplastics) chiếm tỷ lệ cao nhất, được tạo ra từ việc phân hủy các sản phẩm nhựa lớn hơn.'
    },
    {
        'id': 3,
        'question': 'Túi nilon thường được động vật biển nào nhầm lẫn với thức ăn?',
        'options': ['Cá heo', 'Rùa biển', 'Cá mập', 'Cá voi'],
        'correct': 1,
        'explanation': 'Rùa biển thường nhầm lẫn túi nilon với sứa, thức ăn yêu thích của chúng, dẫn đến tử vong.'
    },
    {
        'id': 4,
        'question': 'Mỗi năm có bao nhiêu tấn rác thải nhựa được thải ra đại dương?',
        'options': ['1 triệu tấn', '8 triệu tấn', '15 triệu tấn', '25 triệu tấn'],
        'correct': 1,
        'explanation': 'Mỗi năm có khoảng 8 triệu tấn rác thải nhựa được thải ra đại dương, tương đương 1 xe tải rác mỗi phút.'
    },
    {
        'id': 5,
        'question': 'Lưới đánh cá bỏ hoang được gọi là gì?',
        'options': ['Ghost nets', 'Dead nets', 'Lost nets', 'Ocean nets'],
        'correct': 0,
        'explanation': 'Lưới đánh cá bỏ hoang được gọi là "Ghost nets" - chúng tiếp tục bẫy và giết chết động vật biển.'
    },
    {
        'id': 6,
        'question': 'Đầu lọc thuốc lá chứa chất độc hại nào?',
        'options': ['Nicotine', 'Tar', 'Arsenic', 'Tất cả đáp án trên'],
        'correct': 3,
        'explanation': 'Đầu lọc thuốc lá chứa nicotine, tar, arsenic và nhiều chất độc hại khác, gây ô nhiễm nước biển.'
    },
    {
        'id': 7,
        'question': 'Tái chế 1 lon nhôm tiết kiệm được bao nhiêu phần trăm năng lượng?',
        'options': ['50%', '70%', '85%', '95%'],
        'correct': 3,
        'explanation': 'Tái chế 1 lon nhôm tiết kiệm được 95% năng lượng so với sản xuất lon mới từ nguyên liệu thô.'
    },
    {
        'id': 8,
        'question': 'Hiện tượng "Great Pacific Garbage Patch" là gì?',
        'options': ['Đảo rác nhựa', 'Vùng nước ô nhiễm', 'Khu vực tập trung rác', 'Tất cả đáp án trên'],
        'correct': 3,
        'explanation': 'Great Pacific Garbage Patch là khu vực tập trung rác thải nhựa lớn nhất thế giới, có diện tích gấp 3 lần nước Pháp.'
    },
    {
        'id': 9,
        'question': 'Rác thải nhựa ảnh hưởng đến bao nhiêu loài động vật biển?',
        'options': ['100 loài', '300 loài', '600 loài', '1000 loài'],
        'correct': 2,
        'explanation': 'Rác thải nhựa ảnh hưởng đến hơn 600 loài động vật biển thông qua việc ăn phải hoặc bị mắc kẹt.'
    },
    {
        'id': 10,
        'question': 'Cách nào hiệu quả nhất để giảm rác thải đại dương?',
        'options': ['Dọn dẹp bãi biển', 'Giảm sử dụng nhựa', 'Tái chế nhiều hơn', 'Tất cả đáp án trên'],
        'correct': 3,
        'explanation': 'Cần kết hợp tất cả các biện pháp: giảm sử dụng, tái chế và dọn dẹp để bảo vệ đại dương hiệu quả.'
    },
    {
        'id': 11,
        'question': 'Vi nhựa (microplastics) có kích thước nhỏ hơn bao nhiêu?',
        'options': ['1mm', '5mm', '1cm', '5cm'],
        'correct': 1,
        'explanation': 'Vi nhựa được định nghĩa là các hạt nhựa có kích thước nhỏ hơn 5mm, rất khó thu gom và xử lý.'
    },
    {
        'id': 12,
        'question': 'Động vật biển nào bị ảnh hưởng nhiều nhất bởi rác thải nhựa?',
        'options': ['Cá heo', 'Chim biển', 'Rùa biển', 'Cá voi'],
        'correct': 1,
        'explanation': 'Chim biển bị ảnh hưởng nhiều nhất vì chúng thường nhầm lẫn mảnh nhựa với thức ăn và cho con ăn.'
    },
    {
        'id': 13,
        'question': 'Bao lâu để một túi nilon phân hủy hoàn toàn?',
        'options': ['10-20 năm', '50-100 năm', '200-400 năm', '500-1000 năm'],
        'correct': 2,
        'explanation': 'Túi nilon cần 200-400 năm để phân hủy hoàn toàn, trong thời gian đó chúng gây hại cho môi trường.'
    },
    {
        'id': 14,
        'question': 'Nguyên nhân chính gây ra ô nhiễm đại dương là gì?',
        'options': ['Hoạt động công nghiệp', 'Rác thải từ đất liền', 'Tàu thuyền', 'Khoan dầu'],
        'correct': 1,
        'explanation': 'Khoảng 80% rác thải đại dương có nguồn gốc từ đất liền, được đưa ra biển qua sông và gió.'
    },
    {
        'id': 15,
        'question': 'Tác động của rác thải nhựa đến chuỗi thức ăn là gì?',
        'options': ['Chỉ ảnh hưởng động vật lớn', 'Tích tụ độc tố qua các bậc', 'Không ảnh hưởng gì', 'Chỉ ảnh hưởng thực vật'],
        'correct': 1,
        'explanation': 'Rác thải nhựa tích tụ độc tố và được truyền qua các bậc trong chuỗi thức ăn, cuối cùng ảnh hưởng đến con người.'
    },
    {
        'id': 16,
        'question': 'Dự án nào đang dọn dẹp rác thải ở Thái Bình Dương?',
        'options': ['Ocean Cleanup', 'Sea Shepherd', 'Greenpeace', 'WWF'],
        'correct': 0,
        'explanation': 'The Ocean Cleanup là dự án tiên phong sử dụng công nghệ để thu gom rác thải nhựa ở Thái Bình Dương.'
    },
    {
        'id': 17,
        'question': 'Lượng rác thải nhựa trong đại dương sẽ như thế nào vào năm 2050?',
        'options': ['Giảm một nửa', 'Giữ nguyên', 'Tăng gấp đôi', 'Nhiều hơn cá'],
        'correct': 3,
        'explanation': 'Theo dự báo, đến năm 2050 lượng rác thải nhựa trong đại dương sẽ nhiều hơn cả cá nếu không có biện pháp.'
    },
    {
        'id': 18,
        'question': 'Cách nào giúp giảm rác thải nhựa hiệu quả nhất?',
        'options': ['Sử dụng túi vải', 'Mang chai nước riêng', 'Từ chối ống hút nhựa', 'Tất cả đáp án trên'],
        'correct': 3,
        'explanation': 'Kết hợp tất cả các hành động nhỏ trong cuộc sống hàng ngày sẽ tạo ra tác động lớn cho môi trường.'
    },
    {
        'id': 19,
        'question': 'Rác thải nhựa ảnh hưởng đến kinh tế biển như thế nào?',
        'options': ['Giảm du lịch', 'Ảnh hưởng ngư nghiệp', 'Tăng chi phí dọn dẹp', 'Tất cả đáp án trên'],
        'correct': 3,
        'explanation': 'Rác thải nhựa gây thiệt hại kinh tế toàn diện: giảm du lịch, ảnh hưởng ngư nghiệp và tăng chi phí xử lý.'
    },
    {
        'id': 20,
        'question': 'Giải pháp nào bền vững nhất cho vấn đề rác thải đại dương?',
        'options': ['Công nghệ dọn dẹp', 'Thay đổi hành vi tiêu dùng', 'Luật pháp nghiêm khắc', 'Giáo dục môi trường'],
        'correct': 1,
        'explanation': 'Thay đổi hành vi tiêu dùng là giải pháp bền vững nhất, ngăn chặn rác thải từ nguồn gốc.'
    }
]

# Thông điệp hoàn thành game
COMPLETION_MESSAGES = [
    "🎉 Chúc mừng! Bạn đã dọn sạch bãi biển và cứu sống nhiều sinh vật biển!",
    "🌊 Tuyệt vời! Nhờ bạn, đại dương đã sạch hơn và an toàn hơn cho các loài sinh vật!",
    "🐠 Xuất sắc! Bạn đã góp phần bảo vệ ngôi nhà của hàng triệu sinh vật biển!",
    "🏆 Hoàn hảo! Bạn là một chiến binh môi trường thực thụ!",
    "🌟 Tuyệt vời! Hành động của bạn đã tạo ra sự khác biệt lớn cho đại dương!",
    "🎊 Chúc mừng! Bạn đã chứng minh rằng mỗi người đều có thể bảo vệ môi trường!",
    "🐢 Cảm ơn bạn! Rùa biển và các sinh vật khác sẽ an toàn hơn nhờ bạn!",
    "🌈 Tuyệt vời! Bạn đã biến đại dương thành một nơi đẹp và sạch sẽ!"
]

# Thông điệp khuyến khích khi trả lời đúng
CORRECT_ANSWER_MESSAGES = [
    "Chính xác! 🎯",
    "Tuyệt vời! 🌟",
    "Đúng rồi! 👏",
    "Xuất sắc! ⭐",
    "Hoàn hảo! 🎉",
    "Giỏi quá! 💪",
    "Tài giỏi! 🏆",
    "Siêu đỉnh! 🚀"
]

# Thông điệp khuyến khích khi trả lời sai
WRONG_ANSWER_MESSAGES = [
    "Không sao! Hãy học hỏi thêm nhé! 📚",
    "Chưa đúng, nhưng bạn đã cố gắng! 💪",
    "Sai rồi, nhưng đây là cơ hội học tập! 🌱",
    "Chưa chính xác, hãy ghi nhớ thông tin này! 🧠",
    "Không đúng, nhưng kiến thức này rất hữu ích! 💡"
]

# Cấu hình game
GAME_CONFIG = {
    'total_waste_items': 15,  # Tổng số rác cần nhặt
    'time_limit': 300,  # 5 phút (300 giây)
    'min_score_to_win': 100,  # Điểm tối thiểu để thắng
    'bonus_points': {
        'speed_bonus': 5,  # Điểm thưởng khi trả lời nhanh
        'streak_bonus': 10,  # Điểm thưởng khi trả lời đúng liên tiếp
        'completion_bonus': 50  # Điểm thưởng khi hoàn thành
    },
    'difficulty_levels': {
        'easy': {
            'waste_spawn_rate': 3000,  # milliseconds
            'question_time_limit': 30,  # seconds
            'points_multiplier': 1
        },
        'medium': {
            'waste_spawn_rate': 2000,
            'question_time_limit': 20,
            'points_multiplier': 1.5
        },
        'hard': {
            'waste_spawn_rate': 1000,
            'question_time_limit': 15,
            'points_multiplier': 2
        }
    }
}

# Thông tin về tác động môi trường
ENVIRONMENTAL_FACTS = [
    "Mỗi phút có 1 xe tải rác thải nhựa được đổ xuống đại dương! 🚛",
    "Có hơn 5 nghìn tỷ mảnh nhựa đang trôi nổi trên đại dương! 🌊",
    "90% chim biển có nhựa trong dạ dày của chúng! 🐦",
    "Rác thải nhựa giết chết hơn 1 triệu chim biển mỗi năm! 😢",
    "Đại dương cung cấp 70% lượng oxy chúng ta thở! 🫁",
    "Hơn 3 tỷ người phụ thuộc vào đại dương để sinh sống! 👥",
    "Rạn san hô cung cấp thức ăn cho 25% loài cá biển! 🐠",
    "Tái chế 1 tấn nhựa tiết kiệm 2000 lít dầu! ⛽"
]

