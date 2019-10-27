import React from 'react';
import './FormErrors.css';

const FormErrors = props => (
  <div>
    <ul className="validation-list">
      {
        props.formRules.map(rule => (
          <li
            className={rule.valid ? "success" : "error"}
            key={rule.id}
          >
            {rule.name}
          </li>
        ))
      }
    </ul>
  </div>
);

export default FormErrors;