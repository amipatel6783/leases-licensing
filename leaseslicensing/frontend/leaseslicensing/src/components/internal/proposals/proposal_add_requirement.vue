<template lang="html">
    <div id="proposalRequirementDetail">
        <modal
            transition="modal fade"
            title="Proposed Condition"
            large
            @ok="validateForm()"
            @cancel="close()"
        >
            <div class="container-fluid">
                <div class="row my-3">
                    <form
                        id="requirementForm"
                        class="needs-validation"
                        name="requirementForm"
                        novalidate
                    >
                        <VueAlert v-model:show="showError" type="danger">
                            <!-- eslint-disable-next-line vue/no-v-html -->
                            <strong v-html="errorString"></strong>
                            <!-- eslint-enable -->
                        </VueAlert>
                        <div class="col">
                            <div class="row mb-3">
                                <label class="col-form-label col-sm-3"
                                    >Type</label
                                >
                                <div class="col-sm-9">
                                    <ul class="list-group">
                                        <li class="list-group-item">
                                            <input
                                                v-model="requirement.standard"
                                                class="me-3"
                                                type="radio"
                                                name="requirementType"
                                                :value="true"
                                                @change="
                                                    toggleStandardRequirement
                                                "
                                            /><label class="control-label"
                                                >Standard Requirement
                                            </label>
                                        </li>
                                        <li class="list-group-item">
                                            <input
                                                v-model="requirement.standard"
                                                class="me-3"
                                                type="radio"
                                                name="requirementType"
                                                :value="false"
                                                @change="
                                                    toggleStandardRequirement
                                                "
                                            />
                                            <label class="control-label"
                                                >Free Text Requirement
                                            </label>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <label
                                        class="col-form-label col-sm-3"
                                        :for="
                                            requirement.standard
                                                ? 'standard_requirement'
                                                : 'free_requirement'
                                        "
                                        >Requirement</label
                                    >
                                    <div
                                        v-if="requirement.standard"
                                        class="col-sm-9"
                                    >
                                        <div>
                                            <select
                                                ref="standard_req"
                                                v-model="
                                                    requirement.standard_requirement
                                                "
                                                class="form-control"
                                                name="standard_requirement"
                                                required
                                            >
                                                <option
                                                    v-for="r in requirements"
                                                    :key="r.id"
                                                    :value="r.id"
                                                >
                                                    {{ r.code }} {{ r.text }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                    <div v-else class="col-sm-9">
                                        <textarea
                                            ref="free_req"
                                            v-model="
                                                requirement.free_requirement
                                            "
                                            class="form-control"
                                            name="free_requirement"
                                            required
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <label
                                        class="col-form-label col-sm-3"
                                        for="due_date"
                                        >Due Date</label
                                    >
                                    <div class="col-sm-9">
                                        <input
                                            id="due_date"
                                            ref="due_date"
                                            v-model="requirement.due_date"
                                            type="date"
                                            class="form-control"
                                            required
                                            @change="setReminderDate"
                                        />
                                        <div class="invalid-feedback">
                                            Please select a due date.
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <label
                                        class="col-form-label col-sm-3"
                                        for="reminder_date"
                                        >Reminder Date</label
                                    >
                                    <div class="col-sm-9">
                                        <input
                                            id="reminder_date"
                                            ref="reminder_date"
                                            v-model="requirement.reminder_date"
                                            type="date"
                                            class="form-control"
                                        />
                                    </div>
                                </div>
                            </div>
                            <template v-if="validDueDate">
                                <div class="row mb-3">
                                    <label
                                        class="col-form-label col-sm-3"
                                        for="recurrence"
                                        >Repeating?</label
                                    >
                                    <div
                                        class="col-sm-9 d-flex align-items-center"
                                    >
                                        <div class="form-check">
                                            <input
                                                v-model="requirement.recurrence"
                                                class="form-check-input"
                                                type="checkbox"
                                                name="recurrence"
                                                @change="toggleRecurrence"
                                            />
                                        </div>
                                    </div>
                                </div>
                                <template v-if="requirement.recurrence">
                                    <div class="row mb-3">
                                        <label
                                            class="col-form-label col-sm-3"
                                            for="recurrenceSchedule"
                                            >Repeats</label
                                        >
                                        <div class="col-sm-9">
                                            <div class="row align-items-center">
                                                <div class="col-3">
                                                    <input
                                                        v-model="
                                                            requirement.recurrence_schedule
                                                        "
                                                        class="form-control"
                                                        type="number"
                                                        name="schedule"
                                                        min="1"
                                                    />
                                                </div>
                                                <div class="col-auto px-0">
                                                    time<span
                                                        v-if="
                                                            requirement.recurrence_schedule >
                                                            1
                                                        "
                                                        >s</span
                                                    >
                                                    each
                                                </div>
                                                <div class="col-auto">
                                                    <select
                                                        id="recurrenceSchedule"
                                                        v-model="
                                                            requirement.recurrence_pattern
                                                        "
                                                        class="form-select"
                                                        name="recurrenceSchedule"
                                                    >
                                                        <option
                                                            value="1"
                                                            selected
                                                        >
                                                            Week
                                                        </option>
                                                        <option value="2">
                                                            Month
                                                        </option>
                                                        <option value="3">
                                                            Year
                                                        </option>
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </template>
                            </template>
                        </div>
                    </form>
                </div>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue';
import VueAlert from '@vue-utils/alert.vue';
import { helpers, api_endpoints } from '@/utils/hooks.js';

export default {
    name: 'RequirementDetail',
    components: {
        modal,
        VueAlert,
    },
    props: {
        proposal_id: {
            type: Number,
            required: true,
        },
        requirements: {
            type: Array,
            required: true,
        },
        selectedRequirement: {
            type: Object,
            required: false,
            default: null,
        },
    },
    emits: ['updateRequirements'],
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            requirement: {
                due_date: '',
                reminder_date: '',
                standard: true,
                recurrence: false,
                recurrence_pattern: '1',
                proposal: vm.proposal_id,
            },
            addingRequirement: false,
            updatingRequirement: false,
            validation_form: null,
            type: '1',
            errors: false,
            errorString: '',
            successString: '',
            success: false,
            datepickerOptions: {
                format: 'DD/MM/YYYY',
                showClear: true,
                useCurrent: false,
                keepInvalid: true,
                allowInputToggle: true,
            },
        };
    },
    computed: {
        showError: function () {
            return this.errors;
        },
        validDueDate: function () {
            if (this.requirement.due_date) {
                return true;
            }
            return false;
        },
    },
    mounted: function () {
        this.form = document.forms.requirementForm;
        this.$nextTick(() => {
            // edit existing requirement
            if (this.selectedRequirement && this.selectedRequirement.id) {
                this.requirement = Object.assign({}, this.selectedRequirement);
            } else {
                console.log(this.requirements);
                this.requirement.standard_requirement = this.requirements[0].id;
                this.requirement.due_date = moment().format('YYYY-MM-DD');
                this.requirement.reminder_date = moment().format('YYYY-MM-DD');
            }
        });
    },
    methods: {
        setReminderDate: function () {
            if (this.requirement.due_date) {
                this.requirement.reminder_date = this.requirement.due_date;
            }
        },
        ok: function () {
            this.sendData();
        },
        close: function () {
            this.isModalOpen = false;
        },
        fetchContact: async function (id) {
            const response = await fetch(api_endpoints.contact(id));
            if (response.ok) {
                this.contact = await response.json();
                this.isModalOpen = true;
            } else {
                console.log(response.statusText);
            }
        },
        toggleStandardRequirement: function () {
            var form = document.getElementById('requirementForm');
            if (!this.requirement.standard) {
                this.requirement.standard_requirement = null;
                this.$refs.free_req.focus();
            } else {
                this.requirement.standard_requirement = this.requirements[0].id;
                this.$refs.standard_req.focus();
            }
            form.classList.remove('was-validated');
        },
        toggleRecurrence: function () {
            var form = document.getElementById('requirementForm');
            if (this.requirement.recurrence) {
                this.requirement.recurrence_pattern = '1';
                this.requirement.recurrence_schedule = 1;
            } else {
                this.requirement.recurrence_pattern = null;
                this.requirement.recurrence_schedule = null;
            }
            form.classList.remove('was-validated');
        },
        validateForm: function () {
            let vm = this;
            var form = document.getElementById('requirementForm');

            if (form.checkValidity()) {
                console.log('Form valid');
                vm.sendData();
            } else {
                form.classList.add('was-validated');
                $('#requirementForm').find(':invalid').first().focus();
            }

            return false;
        },
        sendData: async function () {
            this.errors = false;
            if (this.requirement.standard) {
                this.requirement.free_requirement = '';
            } else {
                this.requirement.standard_requirement = '';
                $(this.$refs.standard_req).val(null).trigger('change');
            }
            if (!this.requirement.due_date) {
                this.requirement.due_date = null;
                this.requirement.recurrence = false;
                delete this.requirement.recurrence_pattern;
                this.requirement.recurrence_schedule
                    ? delete this.requirement.recurrence_schedule
                    : '';
            }
            if (this.requirement.id) {
                this.updatingRequirement = true;
                const response = await fetch(
                    helpers.add_endpoint_json(
                        api_endpoints.proposal_requirements,
                        this.requirement.id
                    ),
                    {
                        body: JSON.stringify(this.requirement),
                        method: 'PUT',
                    }
                );
                if (response.ok) {
                    this.updatingRequirement = false;
                    this.$emit('updateRequirements');
                    this.close();
                } else {
                    this.errors = true;
                    this.errorString = await helpers.parseFetchError(response);
                    this.updatingRequirement = false;
                }
            } else {
                this.addingRequirement = true;
                const response = await fetch(
                    api_endpoints.proposal_requirements,
                    {
                        body: JSON.stringify(this.requirement),
                        method: 'POST',
                    }
                );
                if (response.ok) {
                    this.addingRequirement = false;
                    this.close();
                    this.$emit('updateRequirements');
                } else {
                    this.errors = true;
                    this.addingRequirement = false;
                    this.errorString = await helpers.parseFetchError(response);
                }
            }
        },
    },
};
</script>
