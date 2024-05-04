<template>
  <div>
    <p>Username: </p>
    <input v-model="username" placeholder="Enter your username" />

    <p>Password: </p>
    <input v-model="password" placeholder="Enter your password" />

    <button @click="submit">Login</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    submit() {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "username": this.username, "password": this.password })
      };

      fetch('/login', requestOptions)
        .then(response => response.json())
        .then(data => {
          // Handle response data if needed
          console.log(data);
        })
        .catch(error => {
          // Handle errors
          console.error('Error:', error);
        });
    }
  }
};
</script>
