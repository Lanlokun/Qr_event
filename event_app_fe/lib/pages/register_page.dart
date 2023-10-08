// pages/register_page.dart

import 'package:flutter/material.dart';

class RegisterPage extends StatelessWidget {
@override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Center(
        child: Column(
          children: [
            TextField(
              decoration: InputDecoration(hintText: 'Username'),
            ),
            TextField(
              decoration: InputDecoration(hintText: 'Password'),
              obscureText: true,
            ),
            ElevatedButton(
              onPressed: () {
                // Handle login logic here
              },
              child: Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
  }
