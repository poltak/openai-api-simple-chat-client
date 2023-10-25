import os
import sys
import json
from openai import ChatCompletion


def get_response(completion) -> str:
    return completion.choices[0].get("message", {}).get("content")


def get_response_s(completion) -> str:
    return completion.choices[0].get("delta", {}).get("content")


class FileMessageManager:
    msgs = []

    def __init__(self, file_path: str):
        self.file_path = file_path

    def hydrate(self) -> bool:
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    msg = json.loads(line)
                    self.msgs.append(msg)
            return len(self.msgs) > 0
        except FileNotFoundError:
            return False

    def append_msg(self, msg):
        self.msgs.append(msg)
        with open(self.file_path, 'a') as file:
            msg_s = json.dumps(msg)
            file.write(msg_s + '\n')


class Chat:
    def __init__(
        self,
        sys_prompt=None,
        model="gpt-3.5-turbo",
        save_file="my_chat_hist.txt",
    ):
        self.set_model(model)
        self.msg_man = FileMessageManager(save_file)
        existing_msgs = self.msg_man.hydrate()

        if sys_prompt and not existing_msgs:
            self._append_msg('system', sys_prompt)

    def _append_msg(self, role, content, skip_print=False):
        if not skip_print:
            print(f"{role}: {content}\n")
        msg = {"role": role, "content": content}
        self.msg_man.append_msg(msg)

    def set_model(self, model):
        self.model = model

    def ask_stream(self, prompt, **kwargs):
        self._append_msg('user', prompt, skip_print=True)

        total_response = ''
        print(f"assistant: ", end='')
        for chunk in ChatCompletion.create(
            model=self.model,
            messages=self.msg_man.msgs,
            stream=True,
            **kwargs,
        ):
            response = get_response_s(chunk)
            if response:
                print(response, end='')
                total_response += response

        print('\n')
        self._append_msg('assistant', total_response, skip_print=True)

    def ask(self, prompt, **kwargs):
        self._append_msg('user', prompt, skip_print=True)
        completion = ChatCompletion.create(
            model=self.model,
            messages=self.msg_man.msgs,
            **kwargs,
        )
        response = get_response(completion)
        self._append_msg('assistant', response)


def_sys_prompt = "You are the user's personal assistant, helping them work through life problems."


def main():
    def usage():
        print("Usage: chat.py [chat name] [system prompt]")
        sys.exit(1)

    if len(sys.argv) == 2:
        chat_name = sys.argv[1]
        sys_prompt = def_sys_prompt
        gpt4_mode = False
    elif len(sys.argv) == 3:
        chat_name = sys.argv[1]
        sys_prompt = def_sys_prompt if sys.argv[2] == '4' else sys.argv[2]
        gpt4_mode = sys_prompt == '4'
    elif len(sys.argv) == 4:
        chat_name = sys.argv[1]
        sys_prompt = sys.argv[2]
        gpt4_mode = sys.argv[3] == '4'
    else:
        usage()

    chat = Chat(
        sys_prompt=sys_prompt,
        model="gpt-4" if gpt4_mode else "gpt-3.5-turbo",
        save_file=f"{chat_name}.txt",
    )

    # Main conversation loop
    try:
        while True:
            user_prompt = input("user: ")
            chat.ask_stream(user_prompt)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
