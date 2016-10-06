import "babel-polyfill";
import "bootstrap-sass";
import Vue from "vue";
import VueRouter from "vue-router";

import "./ajax"

import makeMessage from "./messages";

Vue.use(VueRouter);

export const app = Vue.extend({});

export const router = new VueRouter();

const routes = {
  "/":{
    component: require("./components/Dashboard"),
  },
  "/auth": {
    //Leave as NOP because the backend handles this
    component: require("./components/NOP"),
  },
  "/admin": {
    //Leave as NOP because the backend handles this
    component: require("./components/NOP"),
  },
};

function onRouterReady() {
  /* Hack to add routes to nav, which is outside of routed area. Spooooky.
   * Uses raw href because v-link only works on elements in vue components
   */
  for(var route in routes){
    if(routes[route].name){
      let name = routes[route].name;
      $(".navbar-dynamic").append(`<li><a href="#/${name}">${name}</a></li>`);
    }
  }
}


router.map(routes);

router.start(app, "#main", onRouterReady);
