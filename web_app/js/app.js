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
      // When the user clicks "back" in the browser, to view the previous search, onpopstate
      // gets triggered
      window.onpopstate = (event) => {
        this.text = event.state.text;
        this.requestRhymes();
      };

      const word = findGetParameter('ord');
      if (word) {
        this.text = word;
        this.requestRhymes();
      } else {
        setTimeout(function() {
          const searchfield = document.querySelector("#search");
          searchfield.focus();
          searchfield.select();
        }, 10);
      }
    },
    methods: {
      requestRhymes: function() {
        /**
         * Post the word to the backend and get rhymes back
         */
        this.loading = true;

        const payload = {text: this.text};

        // Update URL
        history.pushState(
          payload,
          this.text + ' | Nynorsk Rimordbok',
          '/?ord=' + encodeURIComponent(this.text)
        );

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
