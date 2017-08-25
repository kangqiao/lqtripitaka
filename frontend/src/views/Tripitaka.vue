<template>
  <div id="tripitaka-wrapper">
    <IHeader class="iheader"></IHeader>
    <router-view class="main"></router-view>
    <IFooter class="ifooter"></IFooter>
  </div>
</template>
<script>
  import IHeader from '@/components/IHeader';
  import IFooter from '@/components/IFooter';
  export default{
    components:{
      IHeader,
      IFooter
    },
    mounted(){
    }
  }
</script>
<style >
  .tripitaka-wrapper{
    margin: 0 10%;
    text-align: center;
  }
  .iheader{
    display: block;
    position: absolute;
    top: 0;
    background-color: blanchedalmond;
  }
  .main{
    display: block;
    position: relative;
    margin: 0 10% 0  10%;
    text-align: center;
    background-color: gray;
  }
  .ifooter{
    display: block;
    position: absolute;
    bottom: 0;
    background-color: yellow;
  }

</style>
