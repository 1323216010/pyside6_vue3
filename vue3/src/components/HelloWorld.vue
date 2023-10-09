<template>
  <div class="hello">
    <h1>WorkToolBox App</h1>
    <button @click="sendMessage">Send Message to Python</button>
    <div id="app">{{ logAckMsg }}</div>
    <div id="anotherDiv">{{ anotherMsg }}</div>  <!-- 新增的显示区域 -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import getInterface from "../js/channel";

const logAckMsg = ref('');
const anotherMsg = ref('');  // 新增的响应变量
var channel;

onMounted(async () => {
  const channelInterface = await getInterface;
  channelInterface.logAck.connect(str => {
    logAckMsg.value = str;
  });
  channelInterface.anotherSignal.connect(str => {  // 新增的连接
    anotherMsg.value = str;
  });
  channel = channelInterface;
});

  // 创建一个对象
  let person = {
    name: "Bob",
    age: 30,
    city: "New York"
  };

function sendMessage() {
  // 使用JSON.stringify()方法将对象转换为JSON字符串
  let jsonString = JSON.stringify(person);
  channel.log(jsonString);

  // window.pywebchannel.receiveMessageFromVue("Hello from Vue.js!");
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
