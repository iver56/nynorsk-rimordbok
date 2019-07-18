(function() {
  'use strict';

  let app = new Vue({
    el: '#data-wrapper',
    data: {
      text: '',
      searchText: null,
      loading: false,
      result: null
    },
    created: function() {
      // When the user clicks "back" in the browser, to view the previous search, onpopstate
      // gets triggered
      window.onpopstate = (event) => {
        if (event.state && event.state.text) {
          this.text = event.state.text;
          this.requestRhymes(false);
        } else {
          this.text = '';
          this.result = null;
          document.title = 'Nynorsk Rimordbok';
        }

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
      requestRhymes: function(shouldPushState=true) {
        /**
         * Post the word to the backend and get rhymes back
         */
        this.loading = true;
        this.searchText = this.text;
        const payload = {text: this.text};

        // Update URL
        const title = this.text + ' | Nynorsk Rimordbok';
        if(shouldPushState){
          history.pushState(
            payload,
            title,
            '/?ord=' + encodeURIComponent(this.text)
          );
        }
        document.title = title;

        return axios.post('/api/get_rhymes/', payload)
          .then((response) => {
            this.result = response.data;

            // Assign a URL to each rhyme
            for (let rhyme of this.result.rhymes) {
              if (rhyme.word[0] === rhyme.word[0].toUpperCase()) {
                rhyme.url = 'https://no.wikipedia.org/wiki/' + encodeURIComponent(rhyme.word)
              } else {
                // If the first letter is uppercase, it's probably an "egennamn". In that case,
                // we link to Wikipedia
                rhyme.url = 'https://ordbok.uib.no/perl/ordbok.cgi?OPP=' + encodeURIComponent(rhyme.word) + '&ant_nynorsk=5&nynorsk=+&ordbok=nynorsk';
              }
            }
            this.loading = false;
          })
          .catch((error) => {
            this.loading = false;
            console.log(error);
            alert('Server communication error');
          });
      },
      requestRandomWord: function() {
        const payload = { text: this.text };
        const title = this.text + ' | Nynorsk Rimordbok';
        
        history.pushState(
          payload,
          title,
          '/?ord=' + encodeURIComponent(this.text)
        );
        return axios.get('/api/get_random_word/', payload)
          .then((response) => {
            this.text = response.data['random_word'];
            this.requestRhymes();
          });
      },
    }
  });
})();
