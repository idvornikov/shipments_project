<template>
  <div class="hello">
    <h1>{{ title }}</h1>

    <form @submit.prevent="handleAddOrder">
      <input type="text" v-model="newOrderTitle">
      <input type="number" v-model="newOrderPrice">
      <button class="addBtn" type="submit">Add order</button>
    </form>

    <h2>Orders:</h2>

    <form v-if="editModeEnabled" @submit.prevent="handleEditOrder">
      <input type="text" v-model="editedTitle">
      <input type="number" v-model="editedPrice">
      <div class="actions">
        <button class="addBtn" type="submit">Save</button>
        <button class="cancelBtn" type="button" @click="disableEditMode">Cancel</button>
      </div>
    </form>

    <ul v-if="hasOrders" class="orders">
      <li v-for="order in orders" :key="order.id" class="order" @click="enableEditMode(order.id)">
        <h5>{{ order.title }}</h5>
        <p>{{order.price}}</p>
        <button class="deleteBtn" @click.stop="handleDeleteOrder(order.id)">X</button>
      </li>
    </ul>
    <p v-else>The orders list is empty</p>
  </div>
</template>

<script>
export default {
  name: 'TheShipments',
  data() {
    return {
        title: 'My awesome app',
        newOrderTitle: '',
        newOrderPrice: '',
        editedTitle: '',
        editedPrice: '',
        editedOrderId: '',
        editModeEnabled: false,
        orders: []
      }
    },
      computed: {
        hasOrders () {
          return this.orders.length > 0
        }
      },
      created() {
        // Imitate ajax request
        setTimeout(() => {
          this.orders = fetch();
        }, 3000)
      },
      methods: {
        handleDeleteOrder(orderId) {
          this.orders = this.orders.filter(order => order.id !== orderId)
        },
        handleAddOrder() {
          const id = new Date().getTime();

          this.orders.push({
            id,
            title: this.newOrderTitle,
            price: this.newOrderPrice + '$'
          });

          this.newOrderTitle = '';
          this.newOrderPrice = '';


        },
        handleEditOrder() {
          this.orders = this.orders.map(order => {
            if (order.id !== this.editedOrderId) return order

            return {
              ...order,
              title: this.editedTitle,
              price: this.editedPrice + '$'
            }
          })

          this.disableEditMode()
        },
        enableEditMode(orderId) {
          const order = this.orders.find(orderItem => orderItem.id === orderId)

          if (order) {
            this.editedOrderId = order.id
            this.editedTitle = order.title;
            this.editedPrice= parseInt(order.price);
            this.editModeEnabled = true;
          }
        },
        disableEditMode() {
          this.editModeEnabled = false;
          this.editedTitle = '';
          this.editedPrice = '';
          this.editedOrderId = '';
        }
      }
}
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
</style>
