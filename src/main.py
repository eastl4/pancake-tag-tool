import requests
import time

BASE_URL = "https://pancake.vn/api/v1"
POLL_INTERVAL = 5  # Thời gian chờ giữa mỗi lần kiểm tra (giây)

# Danh sách các tag
TAGS = [
    {"tag_id": 0, "color": "#4b5577", "lighten_color": "#c9ccd6", "text": "Kiểm hàng"},
    {"tag_id": 1, "color": "#822ba1", "lighten_color": "#d9bfe2", "text": "Câu hỏi"},
    {"tag_id": 2, "color": "#0d5aff", "lighten_color": "#b6cdff", "text": "Mua hàng"},
    {"tag_id": 3, "color": "#009344", "lighten_color": "#b2dec6", "text": "Đã gửi"},
    {"tag_id": 4, "color": "#38a6f4", "lighten_color": "#c3e4fb", "text": "Hết hàng"},
    {"tag_id": 5, "color": "#bd2727", "lighten_color": "#ebbebe", "text": "Trả hàng"}
]

# Hàm lấy danh sách page
def get_pages(access_token):
    url = f"{BASE_URL}/pages"
    params = {"access_token": access_token}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("categorized", {}).get("activated", [])
    except requests.exceptions.RequestException as e:
        print("Lỗi khi lấy danh sách page:", e)
        return []

# Hàm lấy danh sách hội thoại từ một page
def get_conversations(page_id, access_token):
    url = f"{BASE_URL}/pages/{page_id}/conversations"
    params = {
        "unread_first": "true",
        "type": "false",
        "mode": "NONE",
        "tags": '"ALL"',
        "except_tags": "[]",
        "access_token": access_token,
        "from_platform": "web"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("conversations", [])
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi lấy hội thoại từ page {page_id}:", e)
        return []

# Hàm gửi tag đến hội thoại
def send_tag(page_id, conversation_id, tag, access_token):
    url = f"{BASE_URL}/pages/{page_id}/conversations/{conversation_id}/toggle_tag"
    params = {"access_token": access_token}
    tag_data = {
        "tag_id": tag["tag_id"],
        "value": 1,
        "psid": conversation_id,
        "tag[color]": tag["color"],
        "tag[id]": tag["tag_id"],
        "tag[lighten_color]": tag["lighten_color"],
        "tag[text]": tag["text"]
    }
    try:
        response = requests.post(url, params=params, data=tag_data)
        response.raise_for_status()
        print(f"Tag '{tag['text']}' đã được gửi đến hội thoại {conversation_id}.")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gửi tag '{tag['text']}' đến hội thoại {conversation_id}:", e)

# Hàm chọn page
def choose_pages(pages):
    print("Danh sách pages:")
    for idx, page in enumerate(pages):
        print(f"{idx + 1}. {page.get('name')} (ID: {page.get('id')})")
    selected_indexes = input("Nhập các số thứ tự của pages muốn duyệt (cách nhau bởi dấu phẩy): ")
    try:
        selected_indexes = [int(idx.strip()) - 1 for idx in selected_indexes.split(",")]
        return [pages[idx] for idx in selected_indexes if 0 <= idx < len(pages)]
    except ValueError:
        print("Lỗi: Vui lòng nhập các số hợp lệ.")
        return []

# Hàm chọn tag cho từng page
def choose_tags_for_pages(selected_pages):
    page_tags = {}
    for page in selected_pages:
        print(f"\nChọn tag cho page '{page.get('name')}' (ID: {page.get('id')}):")
        for idx, tag in enumerate(TAGS):
            print(f"{idx + 1}. {tag['text']} (ID: {tag['tag_id']})")
        selected_indexes = input("Nhập các số thứ tự của tags muốn áp dụng (cách nhau bởi dấu phẩy): ")
        try:
            selected_indexes = [int(idx.strip()) - 1 for idx in selected_indexes.split(",")]
            page_tags[page.get("id")] = [TAGS[idx] for idx in selected_indexes if 0 <= idx < len(TAGS)]
        except ValueError:
            print("Lỗi: Vui lòng nhập các số hợp lệ.")
    return page_tags

# Chương trình chính
def main():
    # Nhập access token từ bàn phím
    access_token = input("Nhập ACCESS_TOKEN của bạn: ").strip()

    # Lấy danh sách pages
    pages = get_pages(access_token)
    if not pages:
        print("Không tìm thấy pages nào.")
        return

    # Người dùng chọn page
    selected_pages = choose_pages(pages)
    if not selected_pages:
        print("Không có page nào được chọn.")
        return

    # Người dùng chọn tag cho từng page
    page_tags = choose_tags_for_pages(selected_pages)
    if not page_tags:
        print("Không có tag nào được chọn cho các page.")
        return

    print("\nChương trình đang chạy live...")
    processed_conversations = set()

    # Chạy live
    while True:
        for page in selected_pages:
            page_id = page.get("id")
            page_name = page.get("name")
            print(f"\nĐang kiểm tra page: {page_name} (ID: {page_id})")

            # Lấy danh sách hội thoại
            conversations = get_conversations(page_id, access_token)
            if not conversations:
                print(f"Không có hội thoại mới trên page {page_name}.")
                continue

            # Xử lý từng hội thoại
            for conversation in conversations:
                conversation_id = conversation.get("id")
                seen = conversation.get("seen", 1)

                # Chỉ xử lý các hội thoại chưa được xem (seen == 0) và chưa xử lý
                if seen == 0 and conversation_id not in processed_conversations:
                    print(f"- Hội thoại ID: {conversation_id} chưa được xem. Gắn tag...")
                    for tag in page_tags.get(page_id, []):
                        send_tag(page_id, conversation_id, tag, access_token)

                    # Đánh dấu hội thoại đã được xử lý
                    processed_conversations.add(conversation_id)

        # Chờ trước khi kiểm tra lại
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()