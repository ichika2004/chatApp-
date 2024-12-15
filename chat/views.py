from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .forms import ChatForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat
from django.utils import timezone
from django.http import JsonResponse
from django.utils import timezone
from .models import Chat

# Create your views here.


class ChatCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
    form_class = ChatForm
    model = Chat

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lte=timezone.now()).order_by('posted_at')

def update_chats(request):
    last_id = int(request.GET.get('last_id', 0))  # 取得最後一條訊息的 ID，默認為 0
    # 獲取自上次 ID 以來的新聊天訊息
    new_chats = Chat.objects.filter(id__gt=last_id).order_by('posted_at')

    # 將每條聊天訊息轉換成字典格式
    chat_data = [
        {
            'id': chat.id,
            'user': chat.user.username,
            'message': chat.message,
            'posted_at': chat.posted_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_superuser': chat.user.is_superuser  # 添加是否是管理員的標記
        }
        for chat in new_chats
    ]
    return JsonResponse({'chats': chat_data})
