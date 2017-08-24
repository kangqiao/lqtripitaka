<template>
  <div id="app">
    <Header class="header"></Header>
    <router-view class="main" name="main"></router-view>
    <Footer class="footer"></Footer>
  </div>
</template>
<script>
  import Header from '@/components/Header';
  import Footer from '@/components/Footer';
  export default{
    components:{
      Header,
      Footer
    },
    mounted(){
    }
  }
</script>
<style >
  .header{
    display: block;
    position: absolute;
    top:0;
    background-color: blanchedalmond;
  }
  .footer{
    display: block;
    position: absolute;
    bottom: 0;
    background-color: yellow;
  }

</style>
