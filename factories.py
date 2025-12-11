from dialogs import MessageDialog, ConfirmDialog, ErrorDialog


class DialogFactory:
    """對話窗工廠"""
    
    @staticmethod
    def create_message(title: str, message: str):
        return MessageDialog(title, message)
    
    @staticmethod
    def create_confirm(title: str, message: str):
        return ConfirmDialog(title, message)
    
    @staticmethod
    def create_error(title: str, error_msg: str):
        return ErrorDialog(title, error_msg)