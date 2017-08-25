<template>
  <div class="header-container">
    <span class="title">龙泉大藏经版本</span>
    <router-link class="btn btn-primary" to="/tripitaka/dict">龙泉字典</router-link>
    <router-link class="btn btn-primary" to="/tripitaka/search">检索版本信息</router-link>
    <a class="btn btn-primary" href="javascript:;" @click="go_read">版本阅读</a>
    <a class="btn btn-primary" href="javascript:;" @click="go_login">登录</a>
    <a class="btn btn-primary" href="/xadmin" target="_blank" >后台</a>
  </div>
</template>

<script>
export default {
  name: 'iheader',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  methods:{
    go_read(){
      this.$router.push('/tripitaka/read');
    },
    go_login(){
      this.$router.push('/login');
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
  .header-container{
    display: flex;
    background-color: aqua;
    width: 100%;
    justify-content: flex-end;
    align-items: center;
    .title{
      flex: auto;
      font-size: 20px;
      color: burlywood;
    }
  }
</style>
