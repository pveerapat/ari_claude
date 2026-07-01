import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../../shared/providers/auth_provider.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _phoneCtrl = TextEditingController();
  final _nameCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  final _farmIdCtrl = TextEditingController();
  String _farmerStatus = 'owner';
  bool _obscure = true;

  bool get _requiresFarmId =>
      _farmerStatus == 'owner_family' || _farmerStatus == 'farm_staff';

  @override
  void dispose() {
    _phoneCtrl.dispose();
    _nameCtrl.dispose();
    _passwordCtrl.dispose();
    _farmIdCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    final auth = context.read<AuthProvider>();
    await auth.register(
      phone: _phoneCtrl.text.trim(),
      name: _nameCtrl.text.trim(),
      password: _passwordCtrl.text,
      farmerStatus: _farmerStatus,
      farmId: _requiresFarmId ? _farmIdCtrl.text.trim() : null,
    );
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    if (auth.state == AuthState.authenticated ||
        auth.state == AuthState.pendingApproval) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) Navigator.of(context).popUntil((r) => r.isFirst);
      });
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Create Account')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Farmer status selection
              const Text('I am a:',
                  style: TextStyle(fontWeight: FontWeight.w600)),
              const SizedBox(height: 8),
              ...['owner', 'owner_family', 'farm_staff']
                  .map((status) => RadioListTile<String>(
                        value: status,
                        groupValue: _farmerStatus,
                        title: Text(_statusLabel(status)),
                        subtitle: Text(_statusDescription(status)),
                        onChanged: (v) => setState(() => _farmerStatus = v!),
                      )),
              const SizedBox(height: 16),
              TextFormField(
                controller: _phoneCtrl,
                keyboardType: TextInputType.visiblePassword,
                onTap: () {
                  WidgetsBinding.instance.addPostFrameCallback((_) {
                    Future.delayed(const Duration(milliseconds: 200), () {
                      SystemChannels.textInput
                          .invokeMethod('TextInput.show');
                    });
                  });
                },
                decoration: const InputDecoration(
                  labelText: 'Phone Number',
                  border: OutlineInputBorder(),
                ),
                validator: (v) => (v == null || v.trim().isEmpty)
                    ? 'Phone is required'
                    : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _nameCtrl,
                keyboardType: TextInputType.visiblePassword,
                onTap: () {
                  WidgetsBinding.instance.addPostFrameCallback((_) {
                    Future.delayed(const Duration(milliseconds: 200), () {
                      SystemChannels.textInput.invokeMethod('TextInput.show');
                    });
                  });
                },
                decoration: const InputDecoration(
                  labelText: 'Full Name',
                  border: OutlineInputBorder(),
                ),
                validator: (v) =>
                    (v == null || v.trim().isEmpty) ? 'Name is required' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _passwordCtrl,
                obscureText: _obscure,
                keyboardType: TextInputType.visiblePassword,
                onTap: () {
                  WidgetsBinding.instance.addPostFrameCallback((_) {
                    Future.delayed(const Duration(milliseconds: 200), () {
                      SystemChannels.textInput.invokeMethod('TextInput.show');
                    });
                  });
                },
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(
                        _obscure ? Icons.visibility : Icons.visibility_off),
                    onPressed: () => setState(() => _obscure = !_obscure),
                  ),
                ),
                validator: (v) =>
                    (v == null || v.isEmpty) ? 'Password is required' : null,
              ),
              if (_requiresFarmId) ...[
                const SizedBox(height: 16),
                TextFormField(
                  controller: _farmIdCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Farm ID (ask your farm owner)',
                    border: OutlineInputBorder(),
                    helperText: 'Required to join an existing farm',
                  ),
                  validator: (v) =>
                      _requiresFarmId && (v == null || v.trim().isEmpty)
                          ? 'Farm ID is required'
                          : null,
                ),
              ],
              if (auth.error != null) ...[
                const SizedBox(height: 12),
                Text(auth.error!,
                    style:
                        TextStyle(color: Theme.of(context).colorScheme.error)),
              ],
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: auth.loading ? null : _submit,
                child: auth.loading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2))
                    : const Text('Register'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _statusLabel(String s) {
    switch (s) {
      case 'owner':
        return 'Farm Owner';
      case 'owner_family':
        return 'Owner Family Member';
      case 'farm_staff':
        return 'Farm Staff';
      default:
        return s;
    }
  }

  String _statusDescription(String s) {
    switch (s) {
      case 'owner':
        return 'Create and manage your own farm';
      case 'owner_family':
        return 'Join a farm with an existing Farm ID';
      case 'farm_staff':
        return 'Join a farm as staff with an existing Farm ID';
      default:
        return '';
    }
  }
}
