from dialogs import MessageDialog


class DialogFactory:
    """對話窗工廠"""

    @staticmethod
    def create_message(title: str, message: str):
        # 不加任何 Emoji
        return MessageDialog(title, message)

    @staticmethod
    def create_error(title: str, error_msg: str):
        # 不加 ❌ Emoji，改用純文字
        return MessageDialog(title, error_msg)

    @staticmethod
    def create_confirm(title: str, message: str):
        # 不加 ❓ Emoji，改用純文字
        return MessageDialog(title, message)