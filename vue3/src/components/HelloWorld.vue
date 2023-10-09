<template>
  <div class="hello">
    <h1>Welcome to Your Vue.js App</h1>
    <button @click="sendMessage">Send Message to Python</button>
    <div id="app">{{ logAckMsg }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import getInterface from "../js/channel";

const logAckMsg = ref('');
var channel;

onMounted(async () => {
  const channelInterface = await getInterface;
  channelInterface.logAck.connect(str => {
    logAckMsg.value = str;
  });
  channelInterface.log("Hello world");
  channel = channelInterface;
});

function sendMessage() {
  channel.log("Hello world");
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
