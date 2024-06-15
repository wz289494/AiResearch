from openai import OpenAI

class Model(object):
    def set_token_model(self,token,model):
        # 设置令牌和模型
        self.token = token
        self.client = OpenAI(base_url="https://api.xty.app/v1",api_key=self.token)
        self.model = model

    def response(self,prompt):
        # 获取响应
        response = self.client.chat.completions.create(
            model= self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content

if __name__ == '__main__':
    token = "sk-kzRFpSyfMV1QlDvw9013901b3cF34cB1B538F134524101A0"
    model = "gpt-4-turbo"

    A = Model()
    a = A.set_token_model(token,model)
    b = A.response('您好')
    print(b)
