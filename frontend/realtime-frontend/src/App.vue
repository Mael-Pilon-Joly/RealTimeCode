<template>
  <div>
    <h1>{{ users }}</h1>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: "",
    };

  },
  mounted() {

     fetch("/users/")
      .then((response) => response.text())
      .then((data) => {
        this.users = data;
      });
  },
};

</script>
