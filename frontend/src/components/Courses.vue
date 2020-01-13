<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Courses</h1>
        <hr />
        <br /><br />
        <alert :message="message" v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.course-modal>
          Add Course
        </button>
        <br /><br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Paperback</th>
              <th scope="col">Price</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(course, index) in courses" :key="index">
              <td>{{ course.title }}</td>
              <td>{{ course.author }}</td>
              <td>
                <span v-if="course.paperback">Yes</span>
                <span v-else>No</span>
              </td>
              <td>${{ course.price }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn pill btn-info btn-sm"
                    v-b-modal.course-update-modal
                    @click="editCourse(course)"
                  >
                    Update
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteCourse(course)"
                  >
                    Delete
                  </button>

                  <rave
                    :isProduction="isProduction"
                    :email="email"
                    :amount="course.price"
                    :reference="reference"
                    :rave-key="raveKey"
                    :callback="callback"
                    :close="close"
                    :currency="currency"
                    :country="country"
                    :custom_title="custom.title"
                    :payment_method="paymentMethod"
                  />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <b-modal ref="addCourseModal" id="course-modal" title="Add a new course" hide-footer>
          <b-form @submit="onSubmit" @reset="onReset" class="w-100">
            <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
              <b-form-input
                id="form-title-input"
                type="text"
                v-model="addCourseForm.title"
                required
                placeholder="Enter title"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-author-group" label="Author:" label-for="form-author-input">
              <b-form-input
                id="form-author-input"
                type="text"
                v-model="addCourseForm.author"
                required
                placeholder="Enter author"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-price-group" label="Price:" label-for="form-price-input">
              <b-form-input
                id="form-price-input"
                type="number"
                step="0.01"
                v-model="addCourseForm.price"
                required
                placeholder="Enter price"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-read-group">
              <b-form-checkbox-group v-model="addCourseForm.paperback" id="form-checks">
                <b-form-checkbox value="true">Paperback</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
        </b-modal>
        <b-modal ref="editCourseModal" id="course-update-modal" title="Update" hide-footer>
          <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
            <b-form-group
              id="form-title-edit-group"
              label="Title:"
              label-for="form-title-edit-input"
            >
              <b-form-input
                id="form-title-edit-input"
                type="text"
                v-model="editForm.title"
                required
                placeholder="Enter title"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group
              id="form-author-edit-group"
              label="Author:"
              label-for="form-author-edit-input"
            >
              <b-form-input
                id="form-author-edit-input"
                type="text"
                v-model="editForm.author"
                required
                placeholder="Enter author"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group
              id="form-price-edit-group"
              label="Purchase price:"
              label-for="form-price-edit-input"
            >
              <b-form-input
                id="form-price-edit-input"
                type="number"
                step="0.01"
                v-model="editForm.price"
                required
                placeholder="Enter price"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-read-edit-group">
              <b-form-checkbox-group v-model="editForm.paperback" id="form-checks">
                <b-form-checkbox value="true">Paperback</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>
            <b-button-group>
              <b-button type="submit" variant="primary">Update</b-button>
              <b-button type="reset" variant="danger">Cancel</b-button>
            </b-button-group>
          </b-form>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Alert from "./Alert.vue";
import Rave from "./BuyCourse.vue";

const raveKey = "<INSERT YOUR RAVE PUBLISHABLE KEY HERE>";

export default {
  data() {
    return {
      isProduction: false,
      raveKey: raveKey,
      email: "ugwuraphael@gmail.com",
      amount: "",
      currency: "USD",
      country: "US",
      custom: {
        title: "FullStack Courses"
      },
      paymentMethod: "",
      courses: [],
      addCourseForm: {
        title: "",
        author: "",
        paperback: [],
        price: ""
      },
      editForm: {
        id: "",
        title: "",
        author: "",
        paperback: [],
        price: ""
      },
      message: "",
      showMessage: false
    };
  },
  components: {
    alert: Alert,
    rave: Rave
  },
  computed: {
    reference() {
      let text = "";
      let possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      for (let i = 0; i < 10; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
      return text;
    }
  },
  methods: {
    callback: function(response) {
      if (response.data.tx.status == "successful" && response.data.tx.chargeResponseCode === "00") {
        if (response.data.tx.fraud_status === "ok") {
          alert("Your payment was successful");
        }
      } else {
        alert("Your payment could not be processed. Please try again later");
      }
    },
    close: function() {
      console.log("Payment closed");
    },
    getCourses() {
      const path = "http://localhost:5000/courses";
      axios
        .get(path)
        .then(res => {
          this.courses = res.data.courses;
        })
        .catch(error => {
          console.error(error);
        });
    },
    addCourse(payload) {
      const path = "http://localhost:5000/courses";
      axios
        .post(path, payload)
        .then(() => {
          this.getCourses();
          this.message = "Course Added!";
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getCourses();
        });
    },
    removeCourse(courseID) {
      const path = `http://localhost:5000/courses/${courseID}`;
      axios
        .delete(path)
        .then(() => {
          this.getCourses();
          this.message = "Course removed!";
          this.showMessage = true;
        })
        .catch(error => {
          console.error(error);
          this.getCourses();
        });
    },
    onDeleteCourse(course) {
      this.removeCourse(course.id);
    },
    initForm() {
      this.addCourseForm.title = "";
      this.addCourseForm.author = "";
      this.addCourseForm.paperback = [];
      this.addCourseForm.price = "";
      this.editForm.id = "";
      this.editForm.title = "";
      this.editForm.author = "";
      this.editForm.paperback = [];
      this.editForm.price = "";
    },
    editCourse(course) {
      this.editForm = course;
    },
    onSubmitUpdate(e) {
      e.preventDefault();
      this.$refs.editCourseModal.hide();
      let paperback = false;
      if (this.editForm.paperback[0]) paperback = true;
      const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
        paperback,
        price: this.editForm.price
      };
      this.updateCourse(payload, this.editForm.id);
    },
    updateCourse(payload, courseID) {
      const path = `http://localhost:5000/courses/${courseID}`;
      axios
        .put(path, payload)
        .then(() => {
          this.getCourses();
          this.message = "Course updated!";
          this.showMessage = true;
        })
        .catch(error => {
          console.error(error);
          this.getCourses();
        });
    },
    onSubmit(e) {
      e.preventDefault();
      this.$refs.addCourseModal.hide();
      let paperback = false;
      if (this.addCourseForm.paperback[0]) paperback = true;
      const payload = {
        title: this.addCourseForm.title,
        author: this.addCourseForm.author,
        paperback,
        price: this.addCourseForm.price
      };
      this.addCourse(payload);
      this.initForm();
    },
    onReset(e) {
      e.preventDefault();
      this.$refs.addCourseModal.hide();
      this.initForm();
    },
    onResetUpdate(e) {
      e.preventDefault();
      this.$refs.editCourseModal.hide();
      this.initForm();
      this.getCourses();
    }
  },
  created() {
    this.getCourses();
  }
};
</script>
