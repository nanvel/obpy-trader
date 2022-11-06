<script setup lang="ts">
import { h } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { NMenu } from "naive-ui";
import type { MenuOption } from "naive-ui";

const menuOptions: MenuOption[] = [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: "home",
          },
        },
        "Home"
      ),
    key: "home",
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: "about",
          },
        },
        "About"
      ),
    key: "about",
  },
];

const activeKey = "home";
</script>

<template>
  <header>
    <n-menu
      v-model:value="activeKey"
      mode="horizontal"
      :options="menuOptions"
    />
  </header>

  <RouterView />
</template>

<style scoped></style>
