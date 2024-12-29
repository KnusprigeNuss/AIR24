<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5001/ping';
      axios.get(path)
          .then((res) => {
            console.log(res.data);
            this.msg = res.data;
          })
          .catch((error) => {

            console.error(error);
          });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>

<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>
</template>
