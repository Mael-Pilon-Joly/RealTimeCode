<template>
  <div>
    <p>Username: </p>
    <input v-model="username" placeholder="Pick a username" />

    <p>Password: </p>
    <input v-model="password" placeholder="Pick a password" />

    <p>Email: </p>
    <input v-model="email" placeholder="Provide an email" />

    <button @click="submit">Sign up</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: ''
    };
  },
  methods: {
    submit() {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "username": this.username, "password": this.password, "email": this.email })
      };

      fetch('/users', requestOptions)
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
