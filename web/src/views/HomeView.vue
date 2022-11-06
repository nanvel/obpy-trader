<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { NDataTable } from "naive-ui";

const files = ref(null);

type ObpyFile = {
  Exchange: string;
  Symbol: string;
  Path: string;
};

const columns = [
  {
    title: "Exchange",
    key: "Exchange",
  },
  {
    title: "Symbol",
    key: "Symbol",
  },
  {
    title: "Key",
    key: "Key",
  },
];

axios
  .get("/api/cloud/files")
  .then((data) => (files.value = data["data"]["data"]));
</script>

<template>
  <main>
    <n-data-table :data="files" :columns="columns" v-if="files" />
  </main>
</template>
