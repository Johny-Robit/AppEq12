<template>
  <div class="edit-profile">
    <h1>Edit Profile</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="form.username" />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="form.email" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="form.password" />
      </div>
      <div>
        <label for="confirmPassword">Confirm Password:</label>
        <input type="password" id="confirmPassword" v-model="form.confirmPassword" />
      </div>
      <button type="submit">Save Changes</button>
    </form>
  </div>
</template>

<script>
import { user } from '../auth';

export default {
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    };
  },
  created() {
    this.fetchUserData();
  },
  methods: {
    fetchUserData() {
      this.form.username = user.value.username;
      this.form.email = user.value.email;
    },
    submitForm() {
      if (this.form.password !== this.form.confirmPassword) {
        alert('Passwords do not match!');
        return;
      }
      // Handle form submission logic here
      console.log('Form submitted:', this.form);
      // ...additional logic to update the profile...
    }
  }
};
</script>

<style scoped>
.edit-profile {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 70%;
}
.edit-profile h1 {
  text-align: center;
}
.edit-profile form div {
  margin-bottom: 15px;
  text-align: left;
}
.edit-profile form label {
  display: block;
  margin-bottom: 5px;
}
.edit-profile form input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
.edit-profile form button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.edit-profile form button:hover {
  background-color: #0056b3;
}
</style>
