<template lang="html">
    <div class="container">
        <div v-if="!applicationsLoading" class="row">
            <div class="col-sm-12">
                <form class="form-horizontal" name="personal_form" method="post">
                    <FormSection label="Apply for a" index="propsal_apply_for">
                        <div class="col-sm-6">
                            <div v-if="application_types && application_types.length" class="form-group">
                                <ul class="list-group">
                                    <li v-for="(application_type, index) in application_types" class="list-group-item">
                                        <input class="form-check-input me-1" type="radio" :value="application_type"
                                            v-model="selectedApplication" :aria-label="application_type">
                                        <label :for="application_type.code + '_' + index" style="font-weight:normal">{{
                                            application_type.description }}</label>
                                    </li>
                                </ul>
                            </div>
                            <div v-else>
                                <p>No application types available</p>
                            </div>
                        </div>
                    </FormSection>
                    <FormSection label="on behalf of" index="proposal_apply_on_behalf_of">
                        <div class="col-sm-6">
                            <ul class="list-group">
                                <li class="list-group-item">
                                    <input class="form-check-input me-1" type="radio" name="behalf_of_org" value="myself"
                                        v-model="selectedOrganisation" aria-label="myself">
                                    <label for="myself">Myself (as an individual)</label>
                                </li>
                                <template v-if="linkedOrganisations && linkedOrganisations.length > 0">
                                    <li v-for="(linkedOrganisation, index) in linkedOrganisations" class="list-group-item">
                                        <input class="form-check-input me-1" type="radio" name="behalf_of_org"
                                            :value="linkedOrganisation" v-model="selectedOrganisation"
                                            :aria-label="linkedOrganisation.ledger_organisation_name">
                                        <label :for="linkedOrganisation.ledger_organisation_name">{{
                                            linkedOrganisation.ledger_organisation_name }}</label>
                                    </li>
                                </template>
                                <BootstrapSpinner v-if="loadingOrganisations" class="text-primary" :centerOfScreen="false"
                                    :small="true" />
                                <template v-if="!loadingOrganisations && !linkedOrganisations">
                                    <li class="list-group-item">
                                        <BootstrapAlert class="mb-1 mt-1">
                                            <span class="me-5">
                                                You are not linked to any organisations
                                            </span>
                                            <a class="btn btn-primary btn-sm ms-2" role="button"
                                                href="/account#organisations">Link an
                                                Organisation</a>
                                        </BootstrapAlert>
                                    </li>
                                </template>
                            </ul>
                        </div>
                    </FormSection>
                    <div class="col-sm-12">
                        <button v-if="!creatingProposal" :disabled="isDisabled" @click.prevent="submit()"
                            class="btn btn-primary float-end continue">Continue</button>
                        <BootstrapButtonSpinner v-else class="btn btn-primary float-end continue" :isLoading="true"
                            :centerOfScreen="false" :small="true" />
                    </div>
                </form>
            </div>
        </div>
        <div v-else class="row">
            <div class="col-sm-3">
                <BootstrapSpinner class="text-primary" />
            </div>
        </div>
    </div>
</template>
<script>
import FormSection from '@/components/forms/section_toggle.vue'
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    data: function () {
        let vm = this;
        return {
            applicationsLoading: false,
            loadingOrganisations: false,
            linkedOrganisations: null,
            selectedOrganisation: null,
            selectedApplication: null,
            application_types: [],
            creatingProposal: false,
        }
    },
    components: {
        FormSection
    },
    computed: {
        isLoading: function () {
            return this.loading.length > 0
        },
        isDisabled: function () {
            let disabled = true;
            if (this.selectedOrganisation && this.selectedApplication) {
                disabled = false;
            }
            return disabled;
        },
        alertText: function () {
            let text = '';
            if (this.selectedApplication && this.selectedApplication.description) {
                text = this.selectedApplication.description;
            }
            text = "a " + text;
            return text
        },
    },
    methods: {
        submit: function () {
            swal.fire({
                title: "Create " + this.selectedApplication.description,
                text: "Are you sure you want to create " + this.alertText + "?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Proceed',
                reverseButtons: true,
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2'
                },
            }).then((result) => {
                if (result.isConfirmed) {
                    this.createProposal();
                }
            }, (error) => {
                console.log(error)
            });
        },
        createProposal: async function () {
            this.$nextTick(async () => {
                let res = null;
                try {
                    this.creatingProposal = true;
                    let payload = null;
                    if ('myself' == this.selectedOrganisation) {
                        payload = {
                            "application_type": this.selectedApplication,
                        }
                    } else {
                        payload = {
                            "org_applicant": this.selectedOrganisation.id,
                            "application_type": this.selectedApplication,
                        }
                    }
                    res = await fetch(api_endpoints.proposal, { body: JSON.stringify(payload), method: 'POST' });
                    const resData = await res.json()
                    const proposal = Object.assign({}, resData);
                    this.$router.push({
                        name: "draft_proposal",
                        params: { proposal_id: proposal.id }
                    });
                } catch (error) {
                    console.log(error)
                    await swal.fire({
                        title: "Create Proposal",
                        text: error.body,
                        icon: "error",
                        text: "There was an error attempting to create your application. Please try again later.",

                    });
                    this.$router.go();
                }
            });
        },
        fetchLinkedOrganisations: function (id) {
            let vm = this
            vm.loadingOrganisations = true;
            fetch(api_endpoints.organisations)
                .then(async (response) => {
                    const data = await response.json()
                    if (!response.ok) {
                        const error =
                            (data && data.message) || response.statusText
                        console.log(error)
                        return Promise.reject(error)
                    }
                    vm.linkedOrganisations = data.results
                    console.log(vm.linkedOrganisations)
                    vm.loadingOrganisations = false;
                })
                .catch((error) => {
                    console.error('There was an error!', error)
                })
        },
        fetchApplicationTypes: async function () {
            const response = await fetch(api_endpoints.application_types_dict);
            const resData = await response.json()
            for (let app_type of resData) {
                this.application_types.push(app_type)
            }
            if (1 == this.application_types.length) {
                this.selectedApplication = this.application_types[0];
            }
        },
    },
    created: async function () {
        this.applicationsLoading = true;
        await this.fetchApplicationTypes();
        this.fetchLinkedOrganisations();
        this.applicationsLoading = false;
    },
}
</script>

<style scoped lang="css">
input[type=text],
select {
    width: 40%;
    box-sizing: border-box;

    min-height: 34px;
    padding: 0;
    height: auto;
}

button.continue {
    width: 150px;
}
</style>
