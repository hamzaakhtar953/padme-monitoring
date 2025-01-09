function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('de-DE');
}

function renderRowIds(params) {
  return params.api.getAllRowIds().indexOf(params.id) + 1;
}

function throwErrorBasedOnResponse(error) {
  if (error.response) {
    // Server responded with a status other than 2xx
    throw new Error(
      `Error: ${error.response.status} - ${error.response.data.detail}`
    );
  } else if (error.request) {
    // Request was made but no response received
    throw new Error('Error: No response received from server');
  } else {
    // Something else happened while setting up the request
    throw new Error(`Error: ${error.message}`);
  }
}

export { formatDate, renderRowIds, throwErrorBasedOnResponse };
