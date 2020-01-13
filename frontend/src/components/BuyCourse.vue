<template>
  <div class="rave">
    <button type="button" class="btn btn-primary btn-sm" @click="payWithRave">Purchase</button>
  </div>
</template>

<script>
export default {
  name: "rave",
  props: {
    isProduction: {
      type: Boolean,
      required: false,
      default: false //set to true if you are going live
    },
    email: {
      type: String,
      required: true
    },
    amount: {
      type: String,
      required: true
    },
    raveKey: {
      type: String,
      required: true
    },
    callback: {
      type: Function,
      required: true,
      default: response => {}
    },
    close: {
      type: Function,
      required: true,
      default: () => {}
    },
    currency: {
      type: String,
      default: "USD"
    },
    country: {
      type: String,
      default: "US"
    },
    custom_title: {
      type: String,
      default: ""
    },
    custom_logo: {
      type: String,
      default: ""
    },
    reference: {
      type: String,
      required: true
    },
    payment_method: {
      type: String,
      default: ""
    }
  },
  created() {
    const script = document.createElement("script");
    script.src = !this.isProduction
      ? "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx/api/flwpbf-inline.js"
      : "https://api.ravepay.co/flwv3-pug/getpaidx/api/flwpbf-inline.js";
    document.getElementsByTagName("head")[0].appendChild(script);
  },
  methods: {
    payWithRave() {
      window.getpaidSetup({
        customer_email: this.email,
        amount: this.amount,
        txref: this.reference,
        PBFPubKey: this.raveKey,
        onclose: () => this.close(),
        currency: this.currency,
        country: this.country,
        custom_title: this.custom_title,
        custom_logo: this.custom_logo,
        payment_method: this.payment_method
      });
    }
  }
};
</script>

<style scoped>
.btn {
  margin: 20px;
}
</style>
