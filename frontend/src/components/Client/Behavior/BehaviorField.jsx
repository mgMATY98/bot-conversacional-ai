import "./BehaviorField.css";

function BehaviorField({

    label,

    field,

    config,

    updateField,

    multiline = false,

    rows = 4,

    placeholder = "",

}) {

    return (

        <>

            <label>

                {label}

            </label>

            {

                multiline ?

                    (

                        <textarea

                            rows={rows}

                            placeholder={placeholder}

                            value={config[field] ?? ""}

                            onChange={(e) =>

                                updateField(

                                    field,

                                    e.target.value,

                                )

                            }

                        />

                    )

                    :

                    (

                        <input

                            type="text"

                            placeholder={placeholder}

                            value={config[field] ?? ""}

                            onChange={(e) =>

                                updateField(

                                    field,

                                    e.target.value,

                                )

                            }

                        />

                    )

            }

        </>

    );

}

export default BehaviorField;