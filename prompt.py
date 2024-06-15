from utils import Utils

class Prompt(object):
    def prompt_generator(self,requirements,target_list,content):
        # 生成json返回格式
        target_str = Utils.list_to_jsonstr(target_list)

        # 构造prompt
        prompt = (
            f"!我现在正在一项研究，需要你帮助我对目标语句进行分析：\n"
            f"{content}\n"
            f"!分析的具体需求是：\n"
            f"{requirements}\n"
            f"!上述分析结果需要{target_list}这些变量，用 json 格式返回，全部为str类型,不要出现其他额外的解释，返回的格式是：\n"
            f"{target_str}"
        )

        return prompt

if __name__ == '__main__':
    prompt = Prompt()
    p = prompt.prompt_generator('分析情感',['情感倾向','态度'],'厉害呀')
    print(p)

    # from model import Model
    #
    # token = "sk-kzRFpSyfMV1QlDvw9013901b3cF34cB1B538F134524101A0"
    # model = "gpt-4-turbo"
    #
    # A = Model()
    # a = A.set_token_model(token, model)
    # b = A.response(p)
    # print(b)



