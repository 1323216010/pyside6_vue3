<template>
  <div class="hello">
    <h1>Welcome to Your Vue.js App</h1>
    <button @click="sendMessage">Send Message to Python</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { QWebChannel } from "../js/qwebchannel.js" 

const messageFromPython = ref('')

onMounted(() => {
  new QWebChannel(qt.webChannelTransport, function(channel) {
    // 连接到 Python 的 MyWebChannel 对象
    window.pywebchannel = channel.objects.pywebchannel;

    // 监听 Python 发送的消息
    window.pywebchannel.sendMessageToVue.connect(function(message) {
      // 使用弹窗显示消息
      alert("Message from Python:\n" + message);
      messageFromPython.value = message;
    });
  });
});

function sendMessage() {
  alert("Sending message to Python...");
  window.pywebchannel.receiveMessageFromVue("Hello from Vue.js!");
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
