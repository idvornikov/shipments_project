<template>
  <div class="hello">

    <form @submit.prevent="handleAddOrder" class="orderForm">
      <h2>{{ title }}</h2>
      <div class="row">
        <label>Description</label> <input :class="{invalid: !description}" type="text" v-model="description" />
      </div>
      <div class="row">
        <label>Sender address</label> <input :class="{invalid: !senderAddress}"  type="text" v-model="senderAddress" />
      </div>
      <div class="row">
        <label>Recipient address</label> <input :class="{invalid: !recipientAddress}"  type="text" v-model="recipientAddress" />
      </div>
      <div class="row">
        <label>Date sent</label> <Datepicker :inputClassName="!dateSent ? 'invalid' : null" v-model="dateSent" ></Datepicker>
      </div>
      <div class="row">
        <label>Date delivered</label> <Datepicker :inputClassName="!dateDelivered ? 'invalid' : null" v-model="dateDelivered" ></Datepicker>
      </div>
      <button class="addBtn" type="submit">Add order</button>
    </form>

    <h2>Orders:</h2>

    <form v-if="editModeEnabled" @submit.prevent="handleEditOrder">
      <div class="row">
        <label>Description</label> <input :class="{invalid: !editedDescription}" type="text" v-model="editedDescription" />
      </div>
      <div class="row">
        <label>Sender address</label> <input :class="{invalid: !editedSenderAddress}"  type="text" v-model="editedSenderAddress" />
      </div>
      <div class="row">
        <label>Recipient address</label> <input :class="{invalid: !editedRecipientAddress}"  type="text" v-model="editedRecipientAddress" />
      </div>
      <div class="row">
        <label>Date sent</label> <Datepicker :inputClassName="!editedDateSent ? 'invalid' : null" v-model="editedDateSent" ></Datepicker>
      </div>
      <div class="row">
        <label>Date delivered</label> <Datepicker :inputClassName="!editedDateDelivered ? 'invalid' : null" v-model="editedDateDelivered" ></Datepicker>
      </div>
      <div class="actions">
        <button class="addBtn" type="submit">Save</button>
        <button class="cancelBtn" type="button" @click="disableEditMode">
          Cancel
        </button>
      </div>
    </form>

    <ul v-if="hasOrders" class="orders">
      <li
        v-for="order in orders"
        :key="order.id"
        class="order"
        @click="enableEditMode(order.id)"
      >
        <div>
          <h5><strong>Track number: </strong>{{ order.track_number }}</h5>
          <p><strong>Description: </strong>{{ order.description}}</p>
          <p><strong>Sender Address: </strong>{{ order.sender_address }}</p>
          <p><strong>Recipient Address: </strong>{{ order.recipient_address }}</p>
          <p><strong>Date sent: </strong>{{ order.date_sent }}</p>
          <p><strong>Date delivered: </strong>{{ order.date_delivered }}</p>
        </div>
        <button class="deleteBtn" @click.stop="handleDeleteOrder(order.id)">
          X
        </button>
      </li>
    </ul>
    <p v-else>The orders list is empty</p>
  </div>
</template>

<script>
import {
  getShipments,
  createShipment,
  updateShipment,
  deleteShipment,
} from "@/api";
import Datepicker from "vue3-date-time-picker";
import 'vue3-date-time-picker/dist/main.css'

export default {
  name: "TheShipments",
  components: { Datepicker },
  data() {
    return {
      title: "New order",
      id: "",
      trackNumber: "",
      description: "",
      senderAddress: "",
      recipientAddress: "",
      dateSent: "",
      dateDelivered: "",
      editedTrackNumber: "",
      editedDescription: "",
      editedSenderAddress: "",
      editedRecipientAddress: "",
      editedDateSent: "",
      editedDateDelivered: "",
      editedOrderId: "",
      date: "",
      editModeEnabled: false,
      orders: [],
    };
  },
  computed: {
    hasOrders() {
      return this.orders.length > 0;
    },
  },
  created() {
    this.fetchOrders();
  },

  methods: {
    validateForm() {
      return this.description && this.senderAddress && this.recipientAddress && this.dateSent && this.dateDelivered;
    },
    async fetchOrders() {
      try {
        const orders = await getShipments();
        this.orders = orders.results;
      } catch (err) {
        console.error(err);
      }
    },
    async handleDeleteOrder(orderId) {
      try {
        await deleteShipment(orderId);
        this.orders = this.orders.filter((order) => order.id !== orderId);
      } catch (err) {
        console.error(err);
      }
    },
    async handleAddOrder() {
      const isFormValid = this.validateForm();

      if (!isFormValid) {
        alert('Fill all fields!');
        return
      }
      try {
        const data = {
          description: this.description,
          sender_address: this.senderAddress,
          recipient_address: this.recipientAddress,
          date_sent: this.dateSent,
          date_delivered: this.dateDelivered
        };

        await createShipment(data);

        this.description = "";
        this.senderAddress = "";
        this.recipientAddress = "";
        this.dateSent = "";
        this.dateDelivered = "";
        await this.fetchOrders();
      } catch (err) {
        console.error(err);
      }
    },
    async handleEditOrder() {
      try {
        const orderData = {
          description: this.editedDescription,
          sender_address: this.editedSenderAddress,
          recipient_address: this.editedRecipientAddress,
          date_sent: this.editedDateSent,
          date_delivered: this.editedDateDelivered,
        };

        const orderId = this.editedOrderId;
        await updateShipment(this.editedOrderId, orderData);
        this.disableEditMode();
        const order = this.orders.find((orderItem) => orderItem.id === orderId);
        order.description = orderData.description
        order.sender_address = orderData.sender_address
        order.recipient_address = orderData.recipient_address
        order.date_sent = orderData.date_sent
        order.date_delivired = orderData.date_delivired
      } catch (err) {
        console.error(err);
      }
    },
    enableEditMode(orderId) {
      const order = this.orders.find((orderItem) => orderItem.id === orderId);

      if (order) {
        this.editedDescription = order.description;
        this.editedSenderAddress = order.sender_address;
        this.editedRecipientAddress = order.recipient_address;
        this.editedDateSent = order.date_sent;
        this.editedDateDelivered = order.date_delivered;
        this.editedOrderId = orderId;
        this.editModeEnabled = true;
      }
      console.log(this.editedOrderId);
    },
    disableEditMode() {
      this.editModeEnabled = false;
      this.editedTitle = "";
      this.editedPrice = "";
      this.editedOrderId = "";
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
form {
  display: flex;
  flex-direction: column;
}

form > *:not(:last-child) {
  margin-bottom: 10px;
}

input {
  padding: 5px;
  border: 1px solid lightgray;
  border-radius: 5px;
}

.addBtn {
  border: none;
  background: lightseagreen;
  color: black;
  cursor: pointer;
  outline: none;
  padding: 5px 10px;
  border-radius: 5px;
}

.orders {
  display: flex;
  flex-direction: column;
  list-style: none;
  padding: 0;
  margin: 20px 0;
}

.order {
  display: flex;
  align-items: center;
  border: 2px solid lightsalmon;
  border-radius: 5px;
  padding: 10px;
}

.order h5 {
  margin-right: 10px;
}

.order strong {
  display: inline-block;
  margin-right: 10px;
}

.order:not(:last-child) {
  margin-bottom: 20px;
}

.deleteBtn {
  border: none;
  background: lightcoral;
  color: white;
  font-weight: bold;
  cursor: pointer;
  outline: none;
  padding: 5px 10px;
  border-radius: 5px;
  margin-left: auto;
}

.cancelBtn {
  background-color: white;
  border: 2px solid lightseagreen;
  border-radius: 5px;
  cursor: pointer;
  outline: none;
  padding: 5px 10px;
}
.orderForm {
  border: 1px solid lightsalmon;
  border-radius: 5px;
  padding: 5px;
}
.row {
  display: flex;
}
.invalid {
  border: 1px solid red !important;
}
</style>