<template>
    <div class="associate-container edit-user-container">
        <div>
            <a href="/user?me" class="back-arrow"><img class="arrow" :src="`${baseUrl}/assets/images/temp/back_arrow.png`"/><span>Back to your profile</span></a>
        </div>
        <div class="row">
            <div class="col-md-3">

                <ul class="list-ha">
                    <li>
                        <i class="xline xline-top"></i>
                        <a href="#section_personal_info"><span>Personal Info</span></a>
                    </li>
                    <li>
                        <i class="xline xline-top"></i>
                        <a href="#section_account_info"><span>Account Info</span></a>
                    </li>
                    <li>
                        <i class="xline xline-top"></i>
                        <a href="#section_hackathons"><span>Hackathons</span></a>
                    </li>
                </ul>
            </div>
            <div class="col-md-6 col-xm-10">
                <div class="page-header">
                    <a id="section_personal_info"></a>
                    <h1>Edit your profile</h1>
                </div>
                <h2 class="form-heading">personal info</h2>
                <form v-on:submit.prevent="submit" class="create-account-form">
                    <div class="form-group">
                        <label for="level">Which of the following describes you best?<span class="text-danger">*</span></label>
                        <select class="form-control" id="level" v-model="level">
                            <option value="Professional">Professional</option>
                            <option value="University">University</option>
                            <option value="High School">High school</option>
                        </select>
                    </div>

                    <div class="form-group" v-if="level != 'High School'">
                        <label for="personal-email">Personal Email</label>
                        <input class="form-control" type="email" id="personal-email" v-model="email" />
                        <p>This is used to affiliate you with an
                        organization (based on the email domain). You
                        will be asked to verify your email first.</p>
                    </div>
                    <div class="form-group" v-else>
                        <p>Please email us your high school name at
                            <a href="mailto:halite@halite.io">halite@halite.io</a>
                        to be associated with that high school on the
                        leaderboard.</p>
                    </div>

                    <div class="line-container"><i class="xline xline-top"></i></div>

                    <h2 id="section_account_info" class="form-heading">Account info</h2>

                    <div class="form-group">
                        <label for="country">Username (As shown On Github)</label>
                        <div class="relative-container">
                            <input type="text" class="form-control" placeholder="Enter your username" v-model="username" disabled>
                            <i class="fa fa-lock lock"></i>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="country">Which country will you be playing from?<span class="text-danger">*</span></label>
                        <v-select
                            placeholder="(would prefer not to disclose)"
                            label="label"
                            :on-change="change_country"
                            v-model="selected_country"
                            :options="country_options">
                        </v-select>
                    </div>

                    <div class="form-group" v-if="selected_country">
                        <label for="country">State/province<span class="text-danger">*</span></label>
                        <v-select
                            placeholder="(would prefer not to disclose)"
                            v-model="selected_region"
                            label="label"
                            :options="regions">
                        </v-select>
                    </div>

                    <div class="form-group has-error" v-if="error">
                        <span id="error-help" class="help-block">{{ error }}</span>
                    </div>
                    <a class="cancel-href base" href="#" target="_self">Cancel</a>
                    <button type="submit" class="btn-ha">Update Profile</button>

                    <div class="line-container"><i class="xline xline-top"></i></div>

                    <h2 id="section_hackathons" class="form-heading">Hackathons</h2>
                    <div class="form-group">
                        <label for="hackathon">Join a Hackathon</label>
                        <input type="text" class="form-control" placeholder="Enter hackathon code" v-model="hackathon_code">
                    </div>
                    <button type="button" class="btn-ha" v-on:click="join_hackathon">Join Hackathon</button>
                </form>
            </div>
        </div>

    </div>
</template>

<script>
    import * as api from "../api";
    import vSelect from 'vue-select';
    import {Alert, countries_data} from "../utils";
    import * as utils from "../utils";

    export default {
        name: "EditUserProfile",
        components: {vSelect},
        props: ['baseUrl'],
        data: function() {
            return {
                countries: [],
                country_options: [],
                data: iso3166.data,
                username: '',
                selected_country: null,
                selected_region: null,
                level: "Professional",
                organization: null,
                organizations: [],
                email: '',
                error: null,
                primary:true,
                user: null,
                hackathon_code: null,
            };
        },
        mounted: function(){
            const countries = Object.entries(iso3166.data);
            countries.sort(function(country1, country2) {
                const country1name = country1[1].name;
                const country2name = country2[1].name;
                const country1code = country1[0];
                const country2code = country2[0];
                if (country1code == 'US' && country2code != 'US') return -1;
                if (country2code == 'US' && country1code != 'US') return 1;

                if (country1name < country2name) {
                    return -1;
                }
                else if (country1name === country2name) {
                    return 0;
                }
                else {
                    return 1;
                }
            });

            const codes = {};
            Object.entries(iso3166.codes).forEach((item) => {
                codes[item[1]] = item[0];
            });

            const new_countries = countries.map((item) => {
                return {
                    label: item[1].name,
                    value: codes[item[0]],
                    code: item[0]
                };
            });
            new_countries.unshift({
                value: "NONE",
                code: "NONE",
                label: "(would prefer not to disclose)",
            });
            this.countries = countries;
            this.country_options = new_countries;

            // get current user
            api.me().then((me) => {
                console.log(me);
                // initialize the data
                this.user = me;
                this.level = me.level;
                this.username = me.username;
                // country
                this.selected_country = this.country_options.find((item) =>{
                    return item.value == me.country_code;
                });
                this.selected_region  = this.regions.find((item) =>{
                    return item.value = me.country_subdivision_code;
                });
                console.log(this.selected_country)
            })
        },
        computed: {
            regions: function() {
                if (!this.selected_country) return [];

                const regions = Object.entries(iso3166.data[this.selected_country.code].sub);

                const codes = [];

                regions.sort(function(region1, region2) {
                    const name1 = region1[1].name;
                    const name2 = region2[1].name;
                    if (name1 < name2) {
                        return -1;
                    }
                    else if (name1 === name2) {
                        return 0;
                    }
                    else {
                        return 1;
                    }
                });

                const new_regions = regions.map((item) => {
                    return {
                        label: item[1].name,
                        value: item[0],
                        type: item[1].type
                    }
                });

                new_regions.unshift({
                    value: "NONE",
                    code: "NONE",
                    label: "(would prefer not to disclose)",
                });

                return new_regions;
            },
            country_code: function(){
                return this.selected_country ? this.selected_country.value : null;
            },
            country_region_code: function(){
                return this.selected_region ? this.selected_region.value : null;
            }
        },
        methods: {
            // reset selected region when change the country
            change_country: function(value){
                this.selected_country = value;
                this.selected_region = null;
            },
            get_country: function(){
                const selected_country =  this.country_options.find((item) => {
                    return item.value == this.country_code.value;
                });
                return selected_country;
            },
            submit: function(e) {

                let request = {
                    "level": this.level,
                    "organization_id": this.organization === "NONE" ? null : this.organization,
                };

                if (this.country_code !== "") {
                    const codes = {};

                    // Build conversion table of 2-char country code to 3-char
                    for (let code3 of Object.keys(iso3166.codes)) {
                        codes[iso3166.codes[code3]] = code3;
                    }

                    request["country_code"] = this.country_code;
                    if (this.country_region_code !== "") {
                        request["country_subdivision_code"] = this.country_region_code;
                    }
                }

                if (this.level !== "High School" && this.email) {
                    request["email"] = this.email;
                }

                // send request
                api.update_me(this.user.user_id, request).then(() => {
                    Alert.show('You have updated your profile successfully', 'success');
                    this.gaData("account", "edit-profile-success", "edit-profile-flow");
                }, (error) => {
                    const errorMessage = error.responseJSON ?
                                         error.responseJSON.message :
                                         "Sorry, we couldn't update your profile. Please try again later.";
                    Alert.show(errorMessage, 'error');
                    this.gaData("account", "edit-profile-error", "edit-profile-flow")
                });

            },
            gaData: function(category, action, label) {
                utils.gaEvent(category, action, label);
            },

            join_hackathon: function() {
                if (this.hackathon_code) {
                    api.registerHackathon(this.hackathon_code).then((response) => {
                        let message = "You've signed up for the hackathon!";
                        if (response.responseJSON && response.responseJSON.message) {
                            message = response.responseJSON.message;
                        }
                        Alert.show(message, 'success');
                    }, (err) => {
                        let message = "Sorry, we couldn't sign you up for the hackathon. Please try again later.";
                        if (err.message) {
                            message = err.message;
                        }
                        if (err.responseJSON) {
                            message = err.responseJSON.message;
                        }

                        Alert.show(message, "error");
                    })
                    this.hackathon_code = null;
                }
                else {
                    Alert.show("Please enter the code to join the hackathon.", 'error');
                }
            },
        }
    }
</script>

<style lang="scss" scoped>
</style>
