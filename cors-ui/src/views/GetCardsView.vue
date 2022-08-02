<template>
  <div>
    <button @click="getCards" >Get Cards</button>
    <div class="info"> 
      App URL: {{ location }}<br/>
      Konnektor URL: {{ this.$store.state.konnektorConfig.url }}
    </div>
    <p>{{info}}</p>
    <ul>
      <li v-for="card in cards">
       {{ card }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import axios from "axios";
import { KonnektorAPI } from "../telematik/KonnektorAPI";
import store from "../store";

export default defineComponent({
  name: "GetCards",
  data() {
    return {
      cards: Array<String>(),
      info: "",
      location: window.location,
    }
  },

  methods: {
    getCards(event: Event) {
      const api = new KonnektorAPI(store.state.konnektorConfig);
      this.info = ""
      this.cards = []
      api.getCards().then((response) => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(response.data, "application/xml");
          const nodes = doc.evaluate("//*[local-name()='Card']", doc, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null)
          let cardNode = nodes.iterateNext();
          this.cards = []
          while(cardNode) {
            const el = cardNode as Element
            const cardHandle = doc.evaluate("*[local-name()='CardHandle']", cardNode, null, XPathResult.STRING_TYPE, null)
            const cardType = doc.evaluate("*[local-name()='CardType']", cardNode, null, XPathResult.STRING_TYPE, null)
            this.cards.push(`${cardType.stringValue}: ${cardHandle.stringValue}`)
            cardNode = nodes.iterateNext();
          }
        }
      ).catch( (err) =>
        this.info = err
      )
      
    }
  }
});
</script>

<style scoped>
.info {
  margin-top: 1em;
}
</style>
