export const createShipment = async (data) => {
  const response = await fetch('http://127.0.0.1:8000/api/shipments/', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error('Error when saving shipment')
  }

  return await response.json()
}
export const updateShipment = async (id, data) => {
  const response = await fetch(`http://127.0.0.1:8000/api/shipments/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error('Error when saving shipment')
  }

  return await response.json()
}

export const deleteShipment = async (id) => {
  const response = await fetch(`http://127.0.0.1:8000/api/shipments/${id}/`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error('Error when saving shipment')
  }
}

export const getShipments = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/shipments/');

  if (!response.ok) {
    throw new Error('Error when fetching shipments')
  }

  return await response.json()
}