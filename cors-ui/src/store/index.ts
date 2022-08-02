import { KonnektorConfig } from "@/telematik/KonnektorAPI";
import { createStore } from "vuex";

export interface State {
  konnektorConfig: KonnektorConfig
}

export default createStore<State>({
  state: {
    konnektorConfig: new KonnektorConfig(
      (location.protocol === 'https:' ? "https://konnektor.h3.spilikin.dev" : "http://localhost:8000"),
      "admin",
      "konnektor",
      "MandantId",
      "ClientSystemId",
      "WorkplaceId")
  },
  getters: {},
  mutations: {},
  actions: {},
  modules: {},
});
