import React from 'react';
import DropdownList from 'react-widgets/lib/DropdownList';

const dropdown = ({ label, colNo, data, disabled, input, onChangeFunc, onKeyUp, placeholder, textField, filter, className, valueField, disableErrorMsg, dropUp, meta: { touched, error } }) => (
    <div className={className ? className : 'col-md-' + colNo + ' new__form--element'}>
        {label ? <label>{label}</label> : null}
        <DropdownList
            data={data}
            disabled={disabled}
            value={input.value}
            dropUp={dropUp}
            onChange={val => { onChangeFunc ? onChangeFunc(val, input) : input.onChange(val[valueField ? valueField : "id"]); }}
            onKeyUp={event => onKeyUp ? onKeyUp(event) : null}
            valueField={valueField ? valueField : "id"}
            textField={textField ? textField : "name"}
            placeholder={placeholder}
            filter={filter ? filter : null}
            messages={{ emptyList: "Sonuç bulunamadı." }}
            className={(touched && error ? "error" : "")} />
        {touched && error && (disableErrorMsg ? null : <label className="error">{error}</label>)}
    </div>
);

const input = ({ colNo, label, input, min, max, step, disabled, placeholder, className, type, onKeyUp, maxLength, minLength, disableErrorMsg, meta: { touched, error }, helptext }) => (
    <div className={className ? className : 'col-md-' + colNo + ' new__form--element'}>
        {label ? <label>{label}</label> : null}
        <input
            {...input}
            min={min}
            max={max}
            step={step}
            disabled={disabled}
            placeholder={(placeholder == null ? label : placeholder)}
            type={type}
            maxLength={maxLength ? maxLength : null}
            minLength={minLength ? minLength : null}
            className={"form-control" + (touched && error ? " error" : "")}
            onKeyUp={event => onKeyUp ? onKeyUp(event) : null}
        />
        {touched && error && (disableErrorMsg ? null : <label className="error">{error}</label>)}
        {helptext ? <span className="help-block"><i className="icon-ios-information-outline"></i> {helptext}</span> : ""}
    </div>
);

module.exports = {
    dropdown,
    input
};