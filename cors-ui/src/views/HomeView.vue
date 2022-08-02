<template>
  <div class="home">
    <h1>Proof of Concept for Konnektor with CORS</h1>

    <div>
        Konnektor (proxy) URL:<br>
        <input type="text" v-model="konnektorConfig.url">
        <br>
        Username (Basic Auth):<br>
        <input type="text" v-model="konnektorConfig.username">
        <br>
        Password (Basic Auth):<br>
        <input type="text" v-model="konnektorConfig.password">
        <br>
        Mandant ID:<br>
        <input type="text" v-model="konnektorConfig.mandantId">
        <br>
        Clientsystem ID:<br>
        <input type="text" v-model="konnektorConfig.clientSystemId">
        <br>
        Workplace ID:<br>
        <input type="text" v-model="konnektorConfig.workplaceId">
        <br>
        <button @click="connect">Connect</button>
    </div>
    <div> {{info}} </div>
    <ul>
      <li v-for="service in services">
       {{ service }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from "vue";
import { KonnektorAPI, KonnektorConfig } from "../telematik/KonnektorAPI";
import store, { State } from "../store/index";

export default defineComponent({
  name: "HomeView",
  data() {
    return {
      info: "",
      konnektorConfig: computed<KonnektorConfig>(() => {
        return store.state.konnektorConfig
      }),
      services: Array<String>(),
    }
  },

  methods: {
    connect(event: Event) {
      const api = new KonnektorAPI(store.state.konnektorConfig)
      this.services = []
      this.info = ""
      api.getServices().then( (response) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(response.data, "application/xml");
        const nodes = doc.evaluate("//*[local-name()='Service']", doc, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null)
        let serviceEl = nodes.iterateNext();
        while(serviceEl) {
          this.services.push(`${(serviceEl as Element).getAttribute("Name")}`);
          serviceEl = nodes.iterateNext();
        }
      }).catch(err => this.info = `Error: ${err}`)
    }
  },
});

</script>
