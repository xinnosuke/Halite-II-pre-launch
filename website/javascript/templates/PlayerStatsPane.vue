<template>
  <table class="player-stats-table">
    <tr class="player-stats" v-for="(player, index) in statistics">
      <td :class="'player-stats-name color-' + (parseInt(index) + 1)">
        <span v-if="players[index] && players[index].id" ><a class="player-name-anchor" :href="`/user/?user_id=${(players[index] || {}).id}`">{{(players[index] || {}).name}}</a>:</span>
        <span v-if="!players[index] || !players[index].id">
          <span class="player-name-anchor">{{(players[index] || {}).name}}</span>:
        </span>
      </td>
      <td class="player-stats-break-down">
        <div class="player-stats-bar-container">
          <div class="player-stats-ship">
            <div v-for="i in 20" v-bind:class="{'bar': true, 'bar-1': isActive(i, player.shipsRate)}"></div>
          </div>
          <div class="player-stats-territory">
            <div v-for="i in 20" v-bind:class="{'bar': true, 'bar-2': isActive(i, player.planetsRate)}"></div>
          </div>
        </div>
      </td>
    </tr>

    <tr class="play-stats">
      <td></td>
      <td class="player-stats-legend">
        <p><span class="player-stats-legend-block player-stats-legend-block-1"></span>
          Relative Ship strength</p>
        <p><span class="player-stats-legend-block player-stats-legend-block-2"></span>
          Relative Planets strength</p>
      </td>
    </tr>
  </table>
</template>

<script>
  import Vue from "vue";
  import * as api from "../api";
  import * as libhaliteviz from "../../../libhaliteviz";


  export default {
    name: 'PlayerStatsPane',
    props: ['players', 'statistics'],
    mounted: function(){
      console.log(this.statistics)
    },
    methods: {
      isActive: function(i, rate){
        return i <= rate * 20 ? true : false;
      }
    }
  }

</script>

<style>
</style>