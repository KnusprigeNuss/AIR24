<script setup>
import { ref } from 'vue';

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

const handleFormSubmit = () => {
  console.log("Form submitted with data:", formData.value);
};

const BMIOptions = Array.from({ length: 101 }, (_, i) => i); // Float from 0 to 100
const PhysicalHealthOptions = Array.from({ length: 31 }, (_, i) => i); // 0 to 30
const MentalHealthOptions = Array.from({ length: 31 }, (_, i) => i); // 0 to 30
const SleepTimeOptions = Array.from({ length: 25 }, (_, i) => i); // 0 to 24

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

const DiabeticOptions = [
  "No", "No borderline diabetes", "Yes", "Yes (during pregnancy)"
];

const GenHealthOptions = ["Excellent", "Very Good", "Good", "Fair", "Poor"];

</script>

<template>
  <div class="container mt-4">
    <h2 class="mb-4">Input Form</h2>
    <form @submit.prevent="handleFormSubmit">
      <div class="row">
        <!-- HeartDisease -->
        <div class="col-md-4 mb-3">
          <label for="HeartDisease" class="form-label">Heart Disease</label>
          <select id="HeartDisease" class="form-control" v-model="formData.HeartDisease">
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        <!-- BMI -->
        <div class="col-md-4 mb-3">
          <label for="BMI" class="form-label">BMI</label>
          <select id="BMI" class="form-control" v-model="formData.BMI">
            <option v-for="bmi in BMIOptions" :key="bmi" :value="bmi">{{ bmi }}</option>
          </select>
        </div>

        <!-- Smoking -->
        <div class="col-md-4 mb-3">
          <label for="Smoking" class="form-label">Smoking</label>
          <select id="Smoking" class="form-control" v-model="formData.Smoking">
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        <!-- AlcoholDrinking -->
        <div class="col-md-4 mb-3">
          <label for="AlcoholDrinking" class="form-label">Alcohol Drinking</label>
          <select id="AlcoholDrinking" class="form-control" v-model="formData.AlcoholDrinking">
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        <!-- Stroke -->
        <div class="col-md-4 mb-3">
          <label for="Stroke" class="form-label">Stroke</label>
          <select id="Stroke" class="form-control" v-model="formData.Stroke">
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        <!-- PhysicalHealth -->
        <div class="col-md-4 mb-3">
          <label for="PhysicalHealth" class="form-label">Physical Health</label>
          <select id="PhysicalHealth" class="form-control" v-model="formData.PhysicalHealth">
            <option v-for="health in PhysicalHealthOptions" :key="health" :value="health">{{ health }}</option>
          </select>
        </div>

        <!-- MentalHealth -->
        <div class="col-md-4 mb-3">
          <label for="MentalHealth" class="form-label">Mental Health</label>
          <select id="MentalHealth" class="form-control" v-model="formData.MentalHealth">
            <option v-for="health in MentalHealthOptions" :key="health" :value="health">{{ health }}</option>
          </select>
        </div>

        <!-- DiffWalking -->
        <div class="col-md-4 mb-3">
          <label for="DiffWalking" class="form-label">Difficulty Walking</label>
          <select id="DiffWalking" class="form-control" v-model="formData.DiffWalking">
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        <!-- Sex -->
        <div class="col-md-4 mb-3">
          <label for="Sex" class="form-label">Sex</label>
          <select id="Sex" class="form-control" v-model="formData.Sex">
            <option value="">Select</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </div>

        <!-- AgeCategory -->
        <div class="col-md-4 mb-3">
          <label for="AgeCategory" class="form-label">Age Category</label>
          <select id="AgeCategory" class="form-control" v-model="formData.AgeCategory">
            <option v-for="age in AgeCategoryOptions" :key="age" :value="age">{{ age }}</option>
          </select>
        </div>

        <!-- Race -->
        <div class="col-md-4 mb-3">
          <label for="Race" class="form-label">Race</label>
          <select id="Race" class="form-control" v-model="formData.Race">
            <option v-for="race in RaceOptions" :key="race" :value="race">{{ race }}</option>
          </select>
        </div>

        <!-- Diabetic -->
        <div class="col-md-4 mb-3">
          <label for="Diabetic" class="form-label">Diabetic</label>
          <select id="Diabetic" class="form-control" v-model="formData.Diabetic">
            <option v-for="status in DiabeticOptions" :key="status" :value="status">{{ status }}</option>
          </select>
        </div>

        <!-- PhysicalActivity -->
        <div class="col-md-4 mb-3">
          <label for="PhysicalActivity" class="form-label">Physical Activity</label>
          <select id="PhysicalActivity" class="form-control" v-model="formData.PhysicalActivity">
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        <!-- GenHealth -->
        <div class="col-md-4 mb-3">
          <label for="GenHealth" class="form-label">General Health</label>
          <select id="GenHealth" class="form-control" v-model="formData.GenHealth">
            <option v-for="health in GenHealthOptions" :key="health" :value="health">{{ health }}</option>
          </select>
        </div>

        <!-- SleepTime -->
        <div class="col-md-4 mb-3">
          <label for="SleepTime" class="form-label">Sleep Time</label>
          <select id="SleepTime" class="form-control" v-model="formData.SleepTime">
            <option v-for="time in SleepTimeOptions" :key="time" :value="time">{{ time }}</option>
          </select>
        </div>

        <!-- Asthma -->
        <div class="col-md-4 mb-3">
          <label for="Asthma" class="form-label">Asthma</label>
          <select id="Asthma" class="form-control" v-model="formData.Asthma">
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        <!-- KidneyDisease -->
        <div class="col-md-4 mb-3">
          <label for="KidneyDisease" class="form-label">Kidney Disease</label>
          <select id="KidneyDisease" class="form-control" v-model="formData.KidneyDisease">
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        <!-- SkinCancer -->
        <div class="col-md-4 mb-3">
          <label for="SkinCancer" class="form-label">Skin Cancer</label>
          <select id="SkinCancer" class="form-control" v-model="formData.SkinCancer">
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

      </div>

      <div class="mt-3">
        <button class="btn btn-primary" type="submit">Submit</button>
      </div>
    </form>
  </div>
</template>