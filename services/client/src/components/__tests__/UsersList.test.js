import React from 'react';
import { shallow } from 'enzyme';
import UsersList from '../UsersList';
import renderer from 'react-test-renderer';

const users = [
  {
    'active': true,
    'admin': false,
    'email': 'chun@email.com',
    'username': 'chun',
    'id': 1
  },
  {
    'active': true,
    'admin': false,
    'email': 'tran@email.com',
    'username': 'tran',
    'id': 2
  }
]

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  expect(wrapper.find('h1').get(0).props.children).toBe('All Users');
  const table = wrapper.find('table');
  expect(table.length).toBe(1);
  expect(wrapper.find('thead').length).toBe(1);
  const th = wrapper.find('th');
  expect(th.length).toBe(5);
  expect(th.get(0).props.children).toBe('ID');
  expect(th.get(1).props.children).toBe('Email');
  expect(th.get(2).props.children).toBe('Username');
  expect(th.get(3).props.children).toBe('Active');
  expect(th.get(4).props.children).toBe('Admin');
  expect(wrapper.find('tbody').length).toBe(1);
  expect(wrapper.find('tbody > tr').length).toBe(2);
  const td = wrapper.find('tbody > tr > td');
  expect(td.length).toBe(10);
  expect(td.get(0).props.children).toBe(1);
  expect(td.get(1).props.children).toBe('chun@email.com');
  expect(td.get(2).props.children).toBe('chun');
  expect(td.get(3).props.children).toBe('true');
  expect(td.get(4).props.children).toBe('false');
});

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UsersList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot();
});