import 'package:flutter/material.dart';

class LordsPrayerScreen extends StatefulWidget {
  const LordsPrayerScreen({super.key});

  @override
  State<LordsPrayerScreen> createState() => _LordsPrayerScreenState();
}

class _LordsPrayerScreenState extends State<LordsPrayerScreen> {
  int _version = 0; // 0: 개역개정, 1: 개역한글

  final Map<int, String> _versions = {
    0: '''하늘에 계신 우리 아버지여
이름이 거룩히 여김을 받으시오며
나라이 임하옵시며
뜻이 하늘에서 이루신 대로 땅에서도 이루어지이다

오늘 우리에게 일용할 양식을 주시고
우리가 우리에게 죄 지은 자를 용서하여 준 것 같이
우리 죄를 용서하여 주시고
우리를 시험에 들게 하지 마시고
다만 악에서 구하시옵소서

(나라와 권세와 영광이 아버지께 영원히 있사옵나이다 아멘.)''',
    1: '''하늘에 계신 우리 아버지여
이름이 거룩히 여김을 받으시오며
나라이 임하옵시며
뜻이 하늘에서 이룬 것 같이
땅에서도 이루어지이다

오늘날 우리에게 일용할 양식을 주옵시고
우리가 우리에게 죄 지은 자를 사하여 준 것 같이
우리 죄를 사하여 주옵시고
우리를 시험에 들게 하지 마옵시고
다만 악에서 구하옵소서

(나라와 권세와 영광이 아버지께 영원히 있사옵나이다 아멘.)''',
  };

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    final versionLabel = _version == 0 ? '개역개정' : '개역한글';

    return Scaffold(
      appBar: AppBar(
        title: const Text('주기도문'),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(40),
          child: Semantics(
            label: '주기도문 버전 선택',
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Semantics(
                  button: true,
                  selected: _version == 0,
                  label: '개역개정 버전',
                  child: ChoiceChip(
                    label: const Text('개역개정'),
                    selected: _version == 0,
                    onSelected: (_) => setState(() => _version = 0),
                  ),
                ),
                const SizedBox(width: 8),
                Semantics(
                  button: true,
                  selected: _version == 1,
                  label: '개역한글 버전',
                  child: ChoiceChip(
                    label: const Text('개역한글'),
                    selected: _version == 1,
                    onSelected: (_) => setState(() => _version = 1),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      body: Padding(
        padding: EdgeInsets.all(pad),
        child: SingleChildScrollView(
          child: Semantics(
            label: '주기도문 $versionLabel 본문',
            child: SelectableText(
              _versions[_version]!.trim(),
              style: const TextStyle(fontSize: 18, height: 1.8),
            ),
          ),
        ),
      ),
    );
  }
}
