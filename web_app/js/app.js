(function() {
  'use strict';

  let app = new Vue({
    el: '#data-wrapper',
    data: {
      text: '',
      loading: false,
      result: null
    },
    created: function() {
      console.log('app created')
      setTimeout(function() {
        const searchfield = document.querySelector("#search");
        searchfield.focus();
        searchfield.select();
      }, 10)
    },
    methods: {
      requestRhymes: function() {
        /**
         * Post the word to the backend and get rhymes back
         */
        this.loading = true;

        const payload = {text: this.text};

        return axios.post('/get_rhymes/', payload)
          .then((response) => {
            console.log(response.data);
            this.result = response.data;
            this.loading = false;
          })
          .catch((error) => {
            this.loading = false;
            console.log(error);
            alert('Server communication error');
          });
      },
    }
  });
})();
