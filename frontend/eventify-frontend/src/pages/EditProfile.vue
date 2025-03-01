<template>
  <div class="edit-profile">
    <h1>Edit Description</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label for="description">Description:</label>
        <textarea id="description" v-model="form.description"></textarea>
      </div>
      <div class="buttons">
        <button type="submit">Save Changes</button>
        <button type="button" @click="cancelChanges">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script>
import { user, fetchUserProfile, isLoggedIn, getToken } from '../store/user'; // Import the user store
import { editProfile } from '../api/user'; // Import the editProfile API function

export default {
  data() {
    return {
      form: {
        username: '',
        description: ''
      }
    };
  },
  created() {
    this.fetchUserData();
    this.form.username = localStorage.getItem('username'); // Get username from local storage
  },
  methods: {
    async fetchUserData() {
      await fetchUserProfile();
      this.form.username = user.value.username;
      this.form.description = user.value.description;
    },
    async submitForm() {
      try {
        const token = getToken();
        const profileData = {
          description: this.form.description
        };
        await editProfile(token, profileData);
        await fetchUserProfile();

        this.$router.push('/profile');
      } catch (error) {
        console.error('Failed to update profile:', error);
        alert('Failed to update profile');
      }
    },
    cancelChanges() {
      this.$router.push('/profile');
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
.edit-profile form input,
.edit-profile form textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
.edit-profile form .buttons {
  display: flex;
  justify-content: space-between;
}
.edit-profile form button {
  width: 48%;
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
