import requests


response = requests.get("https://burst.shopifycdn.com/photos/creamy-cold-drink-sits-on-a-wooden-table.jpg?width=1000&format=pjpg&exif=0&iptc=0")
print(response.status_code)

if response.status_code == 200:
    with open("image.jpg", "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print("Hình ảnh đã được tải xuống thành công.")
else:
    print("Lỗi trong quá trình tải xuống hình ảnh.")
