<script setup>
import {ref} from 'vue';
import axios from "axios";

const formData = ref({
  HeartDisease: '',
  BMI: '',
  Smoking: '',
  AlcoholDrinking: '',
  Stroke: '',
  PhysicalHealth: '',
  MentalHealth: '',
  DiffWalking: '',
  Sex: '',
  AgeCategory: '',
  Race: '',
  Diabetic: '',
  PhysicalActivity: '',
  GenHealth: '',
  SleepTime: '',
  Asthma: '',
  KidneyDisease: '',
  SkinCancer: ''
});

const loading = ref(false);
const response = ref(null);

// Handle form submit
const handleFormSubmit = async () => {
  try {
    loading.value = true;
    response.value = null;
    const result = await axios.post('http://localhost:5000/submit', formData.value);

    if (result.data) {
      response.value = result.data;
    } else {
      response.value = 'Unexpected response structure received';
    }
  } catch (error) {
    response.value = 'An error occurred while submitting the form: ' + error;
  } finally {
    loading.value = false;
  }
};


const BMIOptions = Array.from({length: 101}, (_, i) => i); // Float from 0 to 100
const PhysicalHealthOptions = Array.from({length: 31}, (_, i) => i); // 0 to 30
const MentalHealthOptions = Array.from({length: 31}, (_, i) => i); // 0 to 30
const SleepTimeOptions = Array.from({length: 25}, (_, i) => i); // 0 to 24

const AgeCategoryOptions = [
  "18-24", "25-29", "30-34", "35-39",
  "40-44", "45-49", "50-54", "55-59",
  "60-64", "65-69", "70-74", "75-79", "80 or older"
];

const RaceOptions = [
  "American Indian/Alaskan Native",
  "Asian",
  "Black",
  "Hispanic",
  "White",
  "Other"
];
const DiabeticOptionsConsistent = [
  "No",
  "No borderline diabetes",
  "Yes"
];

const PregnancyOption = "Yes (during pregnancy)";

const GenHealthOptions = ["Excellent", "Very Good", "Good", "Fair", "Poor"];

const fillRandomValues = () => {
  formData.value.BMI = BMIOptions[Math.floor(Math.random() * BMIOptions.length)];
  formData.value.Smoking = Math.random() > 0.5 ? "Yes" : "No";
  formData.value.AlcoholDrinking = Math.random() > 0.5 ? "Yes" : "No";
  formData.value.Stroke = Math.random() > 0.5 ? "Yes" : "No";
  formData.value.PhysicalHealth = PhysicalHealthOptions[Math.floor(Math.random() * PhysicalHealthOptions.length)];
  formData.value.MentalHealth = MentalHealthOptions[Math.floor(Math.random() * MentalHealthOptions.length)];
  formData.value.DiffWalking = Math.random() > 0.5 ? "Yes" : "No";
  formData.value.Sex = Math.random() > 0.5 ? "Male" : "Female";
  formData.value.AgeCategory = AgeCategoryOptions[Math.floor(Math.random() * AgeCategoryOptions.length)];
  formData.value.Race = RaceOptions[Math.floor(Math.random() * RaceOptions.length)];

  // Adjust diabetic options based on sex
  const diabeticOptions =
      formData.value.Sex === "Female"
          ? [...DiabeticOptionsConsistent, PregnancyOption]
          : DiabeticOptionsConsistent;

  formData.value.Diabetic = diabeticOptions[Math.floor(Math.random() * diabeticOptions.length)];

  formData.value.PhysicalActivity = Math.random() > 0.5 ? "Yes" : "No";
  formData.value.GenHealth = GenHealthOptions[Math.floor(Math.random() * GenHealthOptions.length)];
  formData.value.SleepTime = SleepTimeOptions[Math.floor(Math.random() * SleepTimeOptions.length)];
  formData.value.Asthma = Math.random() > 0.5 ? "Yes" : "No";
  formData.value.KidneyDisease = Math.random() > 0.5 ? "Yes" : "No";
  formData.value.SkinCancer = Math.random() > 0.5 ? "Yes" : "No";

  console.log("Form filled with random data:", formData.value);
};

</script>

<template>
  <div class="container mt-4">
    <h2 class="mb-4">User Health Form</h2>
    <form @submit.prevent="handleFormSubmit">

      <!-- Group 1: Physical Metrics -->
      <section class="mb-4">
        <h4>Physical Metrics</h4>
        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="BMI" class="form-label">BMI (Body Mass Index)</label>
            <input type="range" id="BMI" class="form-range" v-model="formData.BMI" :min="0" :max="100"/>
            <small class="form-text">Selected BMI: {{ formData.BMI }}</small>
          </div>
          <div class="col-md-6 mb-3">
            <label for="SleepTime" class="form-label">Average Sleep Time (Hours)</label>
            <input type="range" id="SleepTime" class="form-range" v-model="formData.SleepTime" :min="0" :max="24"/>
            <small class="form-text">Selected Hours: {{ formData.SleepTime }}</small>
          </div>
        </div>
      </section>

      <!-- Group 2: Medical and General Health -->
      <section class="mb-4">
        <h4>Medical & General Health</h4>
        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="PhysicalHealth" class="form-label">For how many days during the past 30 days was your physical
              health (which includes physical illness and injury) <strong>not</strong> good?</label>
            <input type="range" id="PhysicalHealth" class="form-range" v-model="formData.PhysicalHealth" :min="0"
                   :max="30"/>
            <small class="form-text">Selected Days: {{ formData.PhysicalHealth }}</small>
          </div>
          <div class="col-md-6 mb-3">
            <label for="MentalHealth" class="form-label">For how many days during the past 30 days was your mental
              health (which includes stress, depression, and problems with emotions) <strong>not</strong> good?</label>
            <input type="range" id="MentalHealth" class="form-range" v-model="formData.MentalHealth" :min="0"
                   :max="30"/>
            <small class="form-text">Selected Days: {{ formData.MentalHealth }}</small>
          </div>
          <div class="col-md-6 mb-3">
            <label for="GenHealth" class="form-label">General Health Status</label>
            <select id="GenHealth" class="form-control" v-model="formData.GenHealth">
              <option value="">Select</option>
              <option v-for="option in GenHealthOptions" :key="option" :value="option">{{ option }}</option>
            </select>
          </div>
        </div>
      </section>

      <!-- Group 3: Lifestyle Factors -->
      <section class="mb-4">
        <h4>Lifestyle Factors</h4>
        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="Smoking" class="form-label">Smoking Habit</label>
            <select id="Smoking" class="form-control" v-model="formData.Smoking">
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label for="AlcoholDrinking" class="form-label">Alcohol Consumption</label>
            <select id="AlcoholDrinking" class="form-control" v-model="formData.AlcoholDrinking">
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label for="PhysicalActivity" class="form-label">Engages in Physical Activity?</label>
            <select id="PhysicalActivity" class="form-control" v-model="formData.PhysicalActivity">
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
        </div>
      </section>

      <!-- Group 4: Demographics -->
      <section class="mb-4">
        <h4>Demographics</h4>
        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="Sex" class="form-label">Sex</label>
            <select id="Sex" class="form-control" v-model="formData.Sex">
              <option value="">Select</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label for="AgeCategory" class="form-label">Age Category</label>
            <select id="AgeCategory" class="form-control" v-model="formData.AgeCategory">
              <option value="">Select</option>
              <option v-for="option in AgeCategoryOptions" :key="option" :value="option">{{ option }}</option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label for="Race" class="form-label">Race</label>
            <select id="Race" class="form-control" v-model="formData.Race">
              <option value="">Select</option>
              <option v-for="option in RaceOptions" :key="option" :value="option">{{ option }}</option>
            </select>
          </div>
        </div>
      </section>

      <!-- Group 5: Health Conditions -->
      <section class="mb-4">
        <h4>Health Conditions</h4>
        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="Stroke" class="form-label">Had stroke before?</label>
            <select id="Stroke" class="form-control" v-model="formData.Stroke">
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label for="DiffWalking" class="form-label">Difficulty Walking</label>
            <select id="DiffWalking" class="form-control" v-model="formData.DiffWalking">
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label for="Diabetic" class="form-label">Diabetic Status</label>
            <select id="Diabetic" class="form-control" v-model="formData.Diabetic">
              <option value="">Select</option>
              <option
                  v-for="option in formData.Sex === 'Female' ? [...DiabeticOptionsConsistent, PregnancyOption] : DiabeticOptionsConsistent"
                  :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label for="Asthma" class="form-label">Asthma?</label>
            <select id="Asthma" class="form-control" v-model="formData.Asthma">
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label for="KidneyDisease" class="form-label">Kidney Disease</label>
            <select id="KidneyDisease" class="form-control" v-model="formData.KidneyDisease">
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label for="SkinCancer" class="form-label">Skin Cancer History</label>
            <select id="SkinCancer" class="form-control" v-model="formData.SkinCancer">
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
        </div>
      </section>

      <div class="container text-center mt-3">
        <!-- Button container -->
        <div class="d-flex flex-column align-items-center">
          <!-- Button to fill random values -->
          <button
              type="button"
              class="btn btn-secondary mb-3"
              style="width: 33%;
              min-width: 150px;"
              @click="fillRandomValues">
            Fill Random Values
          </button>

          <!-- Submit button -->
          <button
              type="submit"
              class="btn btn-primary"
              :disabled="loading"
              style="width: 33%; min-width: 150px; min-height: 50px;"
          >
            <span
                v-if="loading"
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
            ></span>
            <span v-if="loading" class="ms-2">Loading...</span>
            <span v-else>Submit</span>
          </button>

          <!-- Add space underneath the submit button -->
          <div style="margin-top: 20px;"></div>
        </div>
      </div>

      <!-- Response Section -->
      <div v-if="response" class="response mt-4">
        <div v-if="response.HeartDisease && response.HeartDisease === 'Yes'">
          <h3 style="color: red; font-weight: bold;">Heart Disease Risk: Yes</h3>
          <p>U will die soon! Glhf</p>

          <!-- Display Drug Recommendations -->
          <div v-if="response.DrugRecommendations && response.DrugRecommendations.length > 0">
            <h4 class="mt-4">Drug Recommendations until you die:</h4>
            <div class="row">
              <div
                  v-for="(drug, index) in response.DrugRecommendations"
                  :key="index"
                  class="col-md-4 mb-4"
              >
                <div class="card h-100">
                  <img
                      :src="drug['Image URL']"
                      alt="Drug Image"
                      class="card-img-top"
                  />
                  <div class="card-body">
                    <h5 class="card-title">{{ drug['Medicine Name'] }}</h5>
                    <p class="card-text">
                      <strong>Manufacturer:</strong> {{ drug.Manufacturer }}
                    </p>
                    <p class="card-text">
                      <strong>Composition:</strong> {{ drug.Composition }}
                    </p>
                    <p class="card-text">
                      <strong>Uses:</strong> {{ drug.Uses }}
                    </p>
                    <p class="card-text">
                      <strong>Side Effects:</strong> {{ drug.Side_effects }}
                    </p>
                    <p class="card-text">
                      <strong>Reviews:</strong> Average: {{ drug['Average Review %'] }}% | Excellent:
                      {{ drug['Excellent Review %'] }}% | Poor: {{ drug['Poor Review %'] }}%
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <h3 style="color: green; font-weight: bold;">Heart Disease Risk: No</h3>
        </div>
        <p>{{ response }}</p>
      </div>
    </form>
  </div>
</template>