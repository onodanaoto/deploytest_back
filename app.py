from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
app = Flask(__name__)
CORS(app)

# OpenAI クライアントの初期化
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        date = data.get('date')
        # 日付から月と日だけを抽出
        month_day = date.split('-')[1:]  # ['11', '24'] のような形式
        month_day_str = f"{int(month_day[0])}月{int(month_day[1])}日"
        
        logger.info(f"Received date: {month_day_str}")

        # GPT-4 Turboでテキスト生成（プロンプトを修正）
        text_response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "あなたは歴史的な出来事について詳しい日本人アシスタントです。"},
                {"role": "user", "content": f"{month_day_str}に起きた歴史上の重要な出来事を1つ、簡潔に教えてください。年代も含めて説明してください。"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        text_content = text_response.choices[0].message.content
        logger.info(f"Generated text: {text_content}")

        # DALL-E 2で画像を生成
        image_response = client.images.generate(
            model="dall-e-2",
            prompt=f"Create an artistic illustration of this historical event: {text_content}. Style: digital art, vibrant colors, historical accuracy",
            n=1,
            size="512x512",
            quality="standard"
        )
        image_url = image_response.data[0].url
        logger.info(f"Generated image URL: {image_url}")

        return jsonify({
            'text': text_content,
            'image': image_url
        })

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while processing your request'
        }), 500

# その他のエンドポイントは変更なし
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hello World by Flask'})

@app.route('/get/<int:id>', methods=['GET'])
def get_by_id(id):
    return jsonify({"result": id * 2})

@app.route('/post', methods=['POST'])
def post_data():
    data = request.json
    return jsonify({"echo": data.get('id')})

if __name__ == '__main__':
    app.run(debug=True)